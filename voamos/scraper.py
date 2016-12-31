# libraries
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# native dependencies
import logging
import datetime

# my libs
from flight import Flight
from helper import Helper


class Scraper:
    Logger = logging.getLogger(__name__)

    BASE_URL = 'https://www.google.com/flights/#search;'

    BASE_LIST_PATH = '//*[@id="root"]/div[3]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div/div[3]/div[1]/div/div[2]/div[2]/div[1]/div'
    LIST_SIMPLE_PATH = BASE_LIST_PATH + '/a'
    LIST_MULTIPLE_PATH = BASE_LIST_PATH + '/span'

    REL_PATHS = {
        'PRICE': 'div[1]/div/div[1]',
        'SECOND_COL': 'div[2]/div',
        'DEP_HOURS': 'span[1]',
        'ARR_HOURS': 'span[2]',
        'AIRLINE': 'span',
        'DURATION': 'div[3]/div[1]',
        'FROM_TO': 'div[3]/div[2]',
        'N_SCALES': 'div[4]/div[1]'
    }

    driver = None

    def __init__(self, driver_name='firefox', driver_path=None):
        self.Logger.info('driver name: {}. driver path: {}'.format(driver_name, driver_path))

        self.driver_name = driver_name
        self.driver_path = driver_path

        self.width = 700
        self.height = 700
        self.is_initialized = False


    def init_driver(self):
        global driver

        if self.is_initialized:
            return

        if self.driver_name == 'chrome':
            driver = webdriver.Chrome(executable_path=self.driver_path)
        elif self.driver_name == 'phantomjs':
            driver = webdriver.PhantomJS(executable_path=self.driver_path)
        elif self.driver_name == 'firefox':
            driver = webdriver.Firefox(executable_path=self.driver_path)
        else:
            raise Exception(
                'Driver "{}" is not supported'.format(self.driver_name))

        self.is_initialized = True
        driver.set_window_size(self.width, self.height)
        driver.implicitly_wait(5)


    def finish(self):
        if self.is_initialized:
            try:
                driver.quit()
            except Exception as e:
                print 'On finish(). Exception: ', e


    # TODO: get listing of flights with multiple hours ("inline flights")
    def fetch_data(self, f, t, d, r='', is_roundtrip=False):
        try:
            self.validate_input(f, t, d, r)
        except Exception, e:
            raise

        self.init_driver()
        url = self.build_url(f, t, d, r, is_roundtrip)

        driver.get(url)

        flights = []
        flights_elements = self.get_flights_elems()
        for elem in flights_elements:
            flight_dict = {'f': f, 't': t, 'd': d, 'r': r}
            flights.append(self.get_flight_from_elem(elem, flight_dict))

        self.Logger.debug(Helper.print_flights(flights))
        return flights


    def expand_multiple_flights_elems(self):
        multiple_path_elems = driver.find_elements(
            By.XPATH, self.LIST_MULTIPLE_PATH)
        times = len(multiple_path_elems)

        for i in xrange(times):
            multiple_path_elems[i].click()
            multiple_path_elems = driver.find_elements(
                By.XPATH, self.LIST_MULTIPLE_PATH)


    def get_flights_elems(self):
        self.expand_multiple_flights_elems()

        # once all multiple flights elements are expanded, a normal
        # query can be executed in order to get a flight row
        flights_elems = driver.find_elements(By.XPATH, self.LIST_SIMPLE_PATH)

        return flights_elems


    # TODO: handle wifi div messing up with dep/arr hours
    def get_flight_from_elem(self, elem, flight_dict):
        flight_dict = self.get_second_column_values(elem, flight_dict)
        flight_dict['price'] = self.get_price_value(elem)
        flight_dict['duration'] = elem.find_element(
            By.XPATH, self.REL_PATHS['DURATION']).text
        flight_dict['from_to'] = elem.find_element(
            By.XPATH, self.REL_PATHS['FROM_TO']).text
        flight_dict['n_scales'] = elem.find_element(
            By.XPATH, self.REL_PATHS['N_SCALES']).text

        return Flight(flight_dict)


    def get_price_value(self, elem):
        html = elem.find_element(By.XPATH, 
                self.REL_PATHS['PRICE']).get_attribute('innerHTML')
        res = html.replace('&nbsp;', ' ')

        return res


    # get valus as dep/arr hours, airline and if has wifi
    def get_second_column_values(self, elem, flight_dict):
        has_wifi = False
        second_col_elems = elem.find_elements(
            By.XPATH, self.REL_PATHS['SECOND_COL'])
        if len(second_col_elems) > 2:
            has_wifi = True
            second_col_elems.pop(0)

        flight_dict['dep_hours'] = second_col_elems[0].find_element(
            By.XPATH, self.REL_PATHS['DEP_HOURS']).get_attribute('tooltip')
        flight_dict['arr_hours'] = second_col_elems[0].find_element(
            By.XPATH, self.REL_PATHS['ARR_HOURS']).get_attribute('tooltip')
        flight_dict['airline'] = second_col_elems[1].find_element(
            By.XPATH, self.REL_PATHS['AIRLINE']).text
        flight_dict['has_wifi'] = has_wifi

        return flight_dict


    def build_url(self, f, t, d, r, is_roundtrip):
        params = ';'.join(['f=' + f, 't=' + t, 'd=' + d, 'r=' + r])
        result = self.BASE_URL + params

        if not is_roundtrip:
            result += ';tt=o'

        return result


    def validate_input(self, f, t, d, r):
        def validate_codes(codes_str, arg_name):
            res = {
                'has_error': False,
                'arg_name': arg_name,
                'value': codes_str,
                'error_msg': ''
            }

            # TODO: check if 3 digit is really a code
            if len(codes_str) != 3:
                codes = codes_str.split(',')
                for i in xrange(len(codes)):
                    if len(codes[i]) != 3:
                        res['has_error'] = True
                        res['error_msg'] = 'Should be in ABC or ABC,ZXC format'
                        break
            return res


        def validate_date(date_str, arg_name):
            res = {
                'has_error': False,
                'arg_name': arg_name,
                'value': date_str,
                'error_msg': ''
            }

            if not date_str:
                return res

            date = Helper.str_to_date(date_str)
            if date < datetime.date.today():
                res['has_error'] = True
                res['error_msg'] = 'Date is in the past'

            return res

        validate_msgs = []
        validate_msgs.append(validate_codes(f, 'from'))
        validate_msgs.append(validate_codes(t, 'to'))
        validate_msgs.append(validate_date(d, 'departure date'))
        validate_msgs.append(validate_date(r, 'return date'))

        has_error = False
        error_msg = ''
        for i in xrange(len(validate_msgs)):
            msg = validate_msgs[i]
            if msg.get('has_error'):
                has_error = True
                error_msg += ('\n* Invalid argument: "{}" with value "{}". '
                              'Error message is: {}').format(msg['arg_name'], msg['value'], msg['error_msg'])

        if has_error:
            raise Exception(error_msg)

        return True
