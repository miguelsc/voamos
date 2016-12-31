import os
import json
import datetime

from flight import Flight


class CacheManager:
    BASE_FOLDER = '../flights_cache'

    def __init__(self, f, t, d):
        self.f = f
        self.t = t
        self.d = d
        self.filename = self.build_filename()


    def get_flights(self):
        with open(self.filename, 'r') as json_data:
            data = json.load(json_data)

        return [Flight(flight) for flight in data['flights']]


    def save_flights(self, flights):
        # convert to dict if flight come as Flight class
        flights = [f.to_dict() if isinstance(
            f, Flight) else f for f in flights]

        now = str(datetime.datetime.utcnow())
        now = now[:len(now) - 7]
        data = {
            'create_date': now,
            'flights': flights
        }

        if not os.path.exists(os.path.dirname(self.filename)):
            try:
                os.makedirs(os.path.dirname(self.filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise Error('Error creating cache dir')

        with open(self.filename, 'w') as outfile:
            json.dump(data, outfile, indent=True)


    def flights_in_cache(self):
        return os.path.isfile(self.filename)
        

    def build_filename(self):
        from_to_folder = '{}_{}'.format(self.f, self.t)
        filename = '{}_{}_{}.json'.format(self.f, self.t, self.d)

        return '{}/{}/{}'.format(self.BASE_FOLDER, from_to_folder, filename)
