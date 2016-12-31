import json
import logging
import pkg_resources


class AirportsManager:

    Logger = logging.getLogger(__name__)

    AIRPORTS_USER_CONF_FILENAME = pkg_resources.resource_filename('voamos', 'data/airports_conf.json')
    AIRPORTS_DB_FILENAME = pkg_resources.resource_filename('voamos', 'data/airports.json')

    def __init__(self,
                 airports_user_conf_filename=None,
                 airports_db_filename=None):

        self.airports_user_conf_filename = airports_user_conf_filename or self.AIRPORTS_USER_CONF_FILENAME
        self.airports_db_filename = airports_db_filename or self.AIRPORTS_DB_FILENAME

        self.airports_user_conf_data = None
        self.airports_db_data = None


    def get_airports_by_city(self, city, country=None, continent=None):
        city_aiports = self._get_user_conf_airports_by_city(
            city, country, continent)
        if len(city_aiports) == 0:
            city_aiports = self._get_db_airports_by_city(
                city, country, continent)

        return city_aiports


    def get_airports_codes_by_city(self, city, country=None, continent=None):
        if not city:
            raise Exception('No city given', city)

        city_airports = self.get_airports_by_city(city, country, continent)

        return [airport['iata'] for airport in city_airports if airport['iata']]


    def _get_user_conf_airports_by_city(self, city, country, continent):
        if self.airports_user_conf_data is None:
            self.__open_airports_user_conf_file()

        def concat_object_lists(data_object):
            data = {}
            for key in data_object.keys():
                for k in data_object[key]:
                    data[k] = data_object[key][k]
            return data

        def get_level_data(data, key, name=''):
            if key is not None:
                result_data = data.get(key.lower(), {})
                self.Logger.debug('%s was given', name)
            else:
                result_data = concat_object_lists(data)
                self.Logger.debug('%s was NOT given', name)
            return result_data

        continent_data = get_level_data(
            self.airports_user_conf_data, continent, 'continent')
        self.Logger.debug('continent data: %s', continent_data)

        country_data = get_level_data(continent_data, country, 'country')
        self.Logger.debug('country data: %s', country_data)

        return country_data.get(city.lower(), [])


    def _get_db_airports_by_city(self, city, country, continent):
        city_aiports = []

        if self.airports_db_data is None:
            self.__open_airports_db_file()

        for airport_key in self.airports_db_data:
            airport = self.airports_db_data[airport_key]

            country_condition = (country.lower() == airport[
                                 'country'].lower()) if country is not None else True
            continent_condition = (continent.lower() in airport[
                                   'tz'].lower()) if continent is not None else True

            if airport['city'] == city and country_condition and continent_condition:
                city_aiports.append(airport)

        return city_aiports


    def __open_airports_user_conf_file(self):
        with open(self.airports_user_conf_filename, 'r') as airports_user_conf_json_data:
            self.airports_user_conf_data = json.load(
                airports_user_conf_json_data)
            

    def __open_airports_db_file(self):
        with open(self.airports_db_filename, 'r') as airports_db_json_data:
            self.airports_db_data = json.load(airports_db_json_data)
