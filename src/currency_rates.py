#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, re, urllib2, utils, logging
import webapp2
from google.appengine.api import memcache

NOT_SUPPORTED_RATE = -1

class GoogleCurrencyRateRequest():
    def get_rate(self, from_currency, to_currency):
        rate = None
        url = 'https://www.google.com/ig/calculator?hl=en&q={0}{1}=?{2}'.format(1, from_currency, to_currency)
        opener = urllib2.build_opener()
        urllib2.install_opener(opener)

        # for normal rate, google returns r'{lhs: "1 U.S. dollar",rhs: "21 276.5957 Vietnamese dong",error: "",icc: true}'
        # for small rate, google returns r'{lhs: "1 Vietnamese dong",rhs: "4.7 \x26#215; 10\x3csup\x3e-5\x3c/sup\x3e U.S. dollars",error: "",icc: true}'
        response_str = urllib2.urlopen(url).read().decode('utf-8', 'ignore')
        response_str = response_str.decode('string-escape') # decode to r'{lhs: "1 Vietnamese dong",rhs: "4.7 &#215; 10<sup>-5</sup> U.S. dollars",error: "",icc: true}'

        response_str = response_str.replace('lhs:', '"lhs":')
        response_str = response_str.replace('rhs:', '"rhs":')
        response_str = response_str.replace('error:', '"error":')
        response_str = response_str.replace('icc:', '"icc":')

        converted = json.loads(response_str)

        pattern = re.compile('^(?P<rate>[\d ]+\.\d+)\s(?:&#215; 10<sup>(?P<exponential>-?[\d]+)</sup> )?')
        err = converted['error']
        if (err == ''):
            m = pattern.match(converted['rhs'])
            if (m is not None):
                rate = float(re.sub(r' ', '', m.group('rate')))
                exponential = 0
                if m.group('exponential') is not None:
                    exponential = int(m.group('exponential'))
                rate = rate * pow(10, exponential)
            else:
                rate = NOT_SUPPORTED_RATE
        elif (converted['error'] == '4'):
            rate = NOT_SUPPORTED_RATE

        return (rate, err)

class CurrencyRates(webapp2.RequestHandler):
    def get(self):
        request, response = self.request, self.response

        def get_request_params():
            def strip(v):
                if v is not None:
                    v = v.strip()
                return v

            return (strip(request.get('from')), strip(request.get('to')), strip(request.get('q')), strip(request.get('callback')))

        def get_rate(from_currency, to_currency):
            cache_key = '{0}-{1}'.format(from_currency, to_currency)
            rate, err = memcache.get(cache_key), None
            if rate is None:
                req = GoogleCurrencyRateRequest()
                rate, err = req.get_rate(from_currency, to_currency)

                logging.debug('rate fetched, key is {0}'.format(cache_key))

                if rate is not None and memcache.add(cache_key, rate, 600):
                    logging.debug('rate cached, key is {0}'.format(cache_key))
            else:
                logging.debug('rate fetched form cache, key is {0}'.format(cache_key))

            return rate, err

        from_currency, to_currency, qty, callback = get_request_params()

        if not utils.is_none_or_empty(from_currency) and not utils.is_none_or_empty(to_currency):
            rate, err = get_rate(from_currency, to_currency)

            if rate is None:
                result = {"err": err}
            elif rate == NOT_SUPPORTED_RATE:
                result = {"err": 'not supported rate conversion.'}
            else:
                result = {"from": from_currency, "to": to_currency, "rate": rate }

                if (qty is not None and len(qty) > 0):
                    try:
                        qty = float(qty)
                        converted_qty = qty * rate
                        result["v"] = converted_qty
                    except:
                        result["warning"] = "invalid quantity, ignored."
        else:
            result = {"err": "invalid request"}

        utils.write_jsonp_output(response, result, callback)
