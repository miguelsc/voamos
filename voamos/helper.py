import datetime


class Helper:

    @staticmethod
    def str_to_date(str_date):
        year = int(str_date[:4])
        month = int(str_date[5:7])
        day = int(str_date[8:])

        return datetime.date(year, month, day)


    @staticmethod
    def add_days_to_date(date, days):
        if isinstance(date, str):
            date = Helper.str_to_date(date)

        new_date = date + datetime.timedelta(days)

        return new_date.strftime('%Y-%m-%d')


    @staticmethod
    def to_int(str):
        new_str = ""
        for c in str:
            if c.isdigit():
                new_str += c

        return int(new_str)


    @staticmethod
    def print_flights(flights_list):
        for flight in flights_list:
            print flight
