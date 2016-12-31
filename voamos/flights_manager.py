import logging

from scraper import Scraper
from cache_manager import CacheManager
from helper import Helper


class FlightsManager:

    Logger = logging.getLogger(__name__)

    def __init__(self, driver=None, driver_path=None):
        self.scraper = Scraper(driver_name=driver, driver_path=driver_path)


    def get_flights(self, f, t, d, r='', ignore_cache=False, close_scraper=True):
        cache_manager = CacheManager(f, t, d)
        flights = []

        if cache_manager.flights_in_cache() and not ignore_cache:
            self.Logger.info(
                "getting flights from {} to {} for {} from Cache".format(f, t, d))
            flights = cache_manager.get_flights()
        else:
            self.Logger.info(
                "getting flights from {} to {} for {} from Browser".format(f, t, d))

            try:
                flights = self.scraper.fetch_data(f, t, d, r)
                cache_manager.save_flights(flights)

                if close_scraper:
                    self.scraper.finish()
            except Exception, e:
                raise

        return flights


    def get_flights_in_range(self, f, t, d, days, ignore_cache=False, close_scraper=True):
        flights_by_day = {}

        for n_days in xrange(days):
            dep_date = Helper.add_days_to_date(d, n_days)
            flights = self.get_flights(
                f, t, dep_date, '', ignore_cache, close_scraper=False)
            flights_by_day[dep_date] = flights

        if close_scraper:
            self.scraper.finish()

        return flights_by_day


    def filter_cheapest_flights(self, flights, n_flights=3):
        self.Logger.info('getting the %d cheapest flights', n_flights)
        return self.sort_by_price(flights)[:n_flights]


    def sort_by_price(self, flights):
        def getKey(flight):
            price = flight.price or 0
            return Helper.to_int(price)

        return sorted(flights, key=getKey)
