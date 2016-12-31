import json
import logging

from flights_manager import FlightsManager
from airports_manager import AirportsManager


class RunnerManager:

    Logger = logging.getLogger(__name__)

    def __init__(self, run_configs_filename, driver=None, driver_path=None):
        self.fm = FlightsManager(driver=driver, driver_path=driver_path)
        self.am = AirportsManager()
        self.run_configs_filename = run_configs_filename

        with open(self.run_configs_filename) as run_configs_json_data:
            self.run_configs_data = json.load(run_configs_json_data)


    def run_conf_set(self):
        success_count = 0
        conf_set = self._get_conf()

        if conf_set is not None:
            self.Logger.info('Running configurations..')
            for i in xrange(len(conf_set)):
                conf = conf_set[i]
                self.Logger.info(
                    'running conf {} of {}'.format(i + 1, len(conf_set)))
                try:
                    self._run_conf(conf)
                    is_success = True
                except Exception, e:
                    self.Logger.error('Exception: {}'.format(e))
                    is_success = False

                success_count = success_count + 1 if is_success else success_count

            self.Logger.info('ran {} of {} with success!'.format(
                success_count, len(conf_set)))


    def _get_conf(self):
        conf = None
        try:
            conf = self.run_configs_data['confs']
        except KeyError as k:
            self.Logger.warning(
                'Could not found configuration object {}'.format(k))
        return conf


    def _run_conf(self, conf):
        from_airport = conf.get('from')
        to_airport = conf.get('to')
        dep_date = conf.get('dep').encode('utf-8')
        days = conf.get('days_range', 0)
        show_n = conf.get('shown_n', 3)

        from_codes = self.am.get_airports_codes_by_city(
            from_airport.get('city'),
            from_airport.get('country'),
            from_airport.get('continent'))
        self.Logger.debug('from codes {}'.format(from_codes))

        to_codes = self.am.get_airports_codes_by_city(
            to_airport.get('city'),
            to_airport.get('country'),
            to_airport.get('continent'))
        self.Logger.debug('to codes {}'.format(to_codes))

        from_codes_str = ','.join(from_codes)
        to_codes_str = ','.join(to_codes)

        flights_by_day = self.fm.get_flights_in_range(
            from_codes_str,
            to_codes_str,
            dep_date,
            days)


    def _get_conf_value(self, object, key):
        conf = None

        try:
            conf = object.get(key)
        except KeyError as k:
            print "Could not find key with name {}".format(k)

        return conf
