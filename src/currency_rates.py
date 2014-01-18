#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, re, urllib2, utils, logging
import webapp2
from google.appengine.api import memcache, urlfetch
from decimal import Decimal, InvalidOperation

NOT_SUPPORTED_RATE = -1

class GoogleCurrencyRateRequest():
    def get_rate(self, from_currency, to_currency):
        rate = None
        url = u'https://www.google.com/ig/calculator?hl=en&q={0}{1}=?{2}'.format(1, urllib2.quote(from_currency), urllib2.quote(to_currency))
        result = urlfetch.fetch(url, deadline=60)

        if result.status_code != 200:
            logging.debug(u'failed to fetch rate info from google, the url is "{0}", the response is {1} {2}.'.format(url, result.status_code, result.content.decode(u'utf-8', u'ignore')))
            return (rate, u'failed to fetch rate info from google, {0} returned.'.format(result.status_code))

        # for normal rate, google returns r'{lhs: "1 U.S. dollar",rhs: "21 276.5957 Vietnamese dong",error: "",icc: true}'
        # for small rate, google returns r'{lhs: "1 Vietnamese dong",rhs: "4.7 \x26#215; 10\x3csup\x3e-5\x3c/sup\x3e U.S. dollars",error: "",icc: true}'
        response_str = result.content.decode(u'utf-8', u'ignore')
        response_str = response_str.replace(r'\x22', r'\\"') # fix issue 9
        response_str = response_str.decode(u'string-escape') # decode to r'{lhs: "1 Vietnamese dong",rhs: "4.7 &#215; 10<sup>-5</sup> U.S. dollars",error: "",icc: true}'

        response_str = response_str.replace(u'lhs:', u'"lhs":')
        response_str = response_str.replace(u'rhs:', u'"rhs":')
        response_str = response_str.replace(u'error:', u'"error":')
        response_str = response_str.replace(u'icc:', u'"icc":')

        converted = json.loads(response_str)

        pattern = re.compile(u'^(?P<rate>[\d ]+\.\d+)\s(?:&#215; 10<sup>(?P<exponential>-?[\d]+)</sup> )?')
        err = converted[u'error']
        if (err == ''):
            m = pattern.match(converted[u'rhs'])
            if (m is not None):
                rate = Decimal(re.sub(r' ', '', m.group(u'rate')))
                exponential = 0
                if m.group(u'exponential') is not None:
                    exponential = int(m.group(u'exponential'))
                rate = rate * pow(10, exponential)
            else:
                rate = NOT_SUPPORTED_RATE
        elif (converted[u'error'] == u'4'):
            rate = NOT_SUPPORTED_RATE

        return (rate, err)

class XeCurrencyRateRequest():
    def get_rate(self, from_currency, to_currency):
        rate, err = None, None
        url = u'http://www.xe.com/ucc/convert.cgi?template=mobile&Amount={0}&From={1}&To={2}'.format(1, urllib2.quote(from_currency), urllib2.quote(to_currency))
        result = urlfetch.fetch(url, deadline=60)

        if result.status_code != 200:
            logging.info(u'failed to fetch rate info from xe.com, the url is "{0}", the response is {1} {2}.'.format(url, result.status_code, result.content.decode(u'utf-8', u'ignore')))
            return (rate, u'failed to fetch rate info from xe.com, {0} returned.'.format(result.status_code))

        response_str = result.content.decode(u'utf-8', u'ignore')
        #logging.info(response_str)

        m = re.search(u'.*>1\s{0}\s=\s(?P<rate>[\d,]+\.\d+)\s{1}.*</td>'.format(from_currency, to_currency), response_str)
        if m:
            #logging.info(m.group(0))
            rate = Decimal(m.group(u'rate').replace(u',', u''))
        else:
            err = 'failed to parse response from xe.com.'

        return (rate, err)

class CurrencyRates(webapp2.RequestHandler):
    def get(self):
        request, response = self.request, self.response

        def get_request_params():
            def strip(v):
                if v is not None:
                    v = v.strip()
                return v

            return (strip(request.get(u'from')), strip(request.get(u'to')), strip(request.get(u'q')), strip(request.get(u'callback')))

        def get_rate(from_currency, to_currency):
            from_currency, to_currency = from_currency.upper(), to_currency.upper()
            cache_key = u'{0}-{1}'.format(from_currency, to_currency)
            rate, err = memcache.get(cache_key), None
            if rate is None:
                req = XeCurrencyRateRequest()
                rate, err = req.get_rate(from_currency, to_currency)

                #logging.debug(u'rate fetched, key is {0}'.format(cache_key))

                if rate is not None and memcache.add(cache_key, rate, 1200):
                    pass
                    #logging.debug(u'rate cached, key is {0}'.format(cache_key))
            else:
                pass
                #logging.debug(u'rate fetched form cache, key is {0}'.format(cache_key))

            return rate, err

        from_currency, to_currency, qty, callback = get_request_params()

        if not utils.is_none_or_empty(from_currency) and not utils.is_none_or_empty(to_currency):
            rate, err = get_rate(from_currency, to_currency)

            if rate is None:
                result = {u'err': err}
            elif rate == NOT_SUPPORTED_RATE:
                result = {u'err': u'not supported rate conversion.'}
            else:
                result = {u'from': from_currency, u'to': to_currency, u'rate': rate }

                if (qty is not None and len(qty) > 0):
                    try:
                        qty = Decimal(qty)
                        converted_qty = qty * rate
                        result[u'v'] = converted_qty
                    except InvalidOperation:
                        result[u'warning'] = u'invalid quantity, ignored.'
        else:
            result = {u'err': u'invalid request'}

        utils.write_jsonp_output(response, result, callback)
