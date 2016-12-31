# -*- coding: utf-8 -*-
import json


class Flight:

    def __init__(self, flight_dict):
        d = flight_dict
        def_value = self.get_value_or_default_from_dict

        self.flight_dict = flight_dict

        self.f = def_value(d, 'f')                       # f: from
        self.t = def_value(d, 't')                       # t: to
        self.d = def_value(d, 'd')                       # d: departure date
        # self.r = def_value(d, 'r')                     # r: return date
        self.price = def_value(d, 'price')               # price: price
        self.airline = def_value(d, 'airline')           # airline: airline
        self.dep_hours = def_value(d, 'dep_hours')       # dep hours: departure hours
        self.arr_hours = def_value(d, 'arr_hours')       # arr hours: arrival hours
        self.duration = def_value(d, 'duration')         # duration: duration of flight
        self.from_to = def_value(d, 'from_to', 
                self.default_f_t(self.f, self.t))        # from_to: str in form of OPO-LIS
        self.n_scales = def_value(d, 'n_scales')         # n_scales: number of scales
        self.has_wifi = def_value(d, 'has_wifi', False)  # was_wifi:


    def __str__(self):
        return " ".join([
            "-------- FLIGHT --------\n",
            "price: {} \n".format(self.price),
            "from - to: {} \n".format(self.from_to),
            "dep date: {} \n".format(self.d),
            "dep hours: {} \n".format(self.dep_hours),
            "arr hours: {} \n".format(self.arr_hours),
            "airline: {} \n".format(self.airline),
            "duration: {} \n".format(self.duration),
            "number scales: {}\n".format(self.n_scales),
            "has wifi: {} \n".format(self.has_wifi)
        ])


    def to_json(self):
        return json.dumps(self.flight_dict, ensure_ascii=False)


    def to_dict(self):
        return self.flight_dict


    def default_f_t(self, f, t):
        return '{}-{}'.format(f, t)


    def get_value_or_default_from_dict(self, dictionary, key, is_encode=True, default=''):
        res = None

        if key in dictionary:
            if is_encode:
                res = dictionary[key].encode('utf-8')
            else:
                res = dictionary[key]
        else:
            res = default

        return res
