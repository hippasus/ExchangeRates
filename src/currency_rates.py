#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import json, re, urllib2, utils
import webapp2

class GoogleCurrencyRateRequest():
    def get_rate(self, from_currency, to_currency):
        rate = None
        url = 'https://www.google.com/ig/calculator?hl=en&q={0}{1}=?{2}'.format(1, from_currency, to_currency)
        opener = urllib2.build_opener()
        urllib2.install_opener(opener)
        
        response_str = urllib2.urlopen(url).read() # {lhs: "1 U.S. dollar",rhs: "7.75019569 Hong Kong dollars",error: "",icc: true}
        response_str = response_str.replace('lhs:', '"lhs":')
        response_str = response_str.replace('rhs:', '"rhs":')
        response_str = response_str.replace('error:', '"error":')
        response_str = response_str.replace('icc:', '"icc":')
        converted = json.loads(response_str)

        pattern = re.compile('(\d+\.\d+) ')
        if (converted['error'] == ''):
            m = pattern.match(converted['rhs'])
            if (m is not None):
                rate = float(m.group(0))

        return rate


class CurrencyRates(webapp2.RequestHandler):
    def get(self):
        request, response = self.request, self.response
        
        def get_request_params():
            return (request.get('from'), request.get('to'), request.get('q'), request.get('callback'))

        from_currency, to_currency, qty, callback = get_request_params()

        if not utils.is_none_or_empty(from_currency) and not utils.is_none_or_empty(to_currency):
            req = GoogleCurrencyRateRequest()

            rate = req.get_rate(from_currency, to_currency)

            if (rate is None):
                result = {"err": 'error occurred'}
            else:
                result = {"from": from_currency, "to": to_currency, "rate": rate }

                if (qty is not None and len(qty) > 0):
                    qty = float(qty)
                    converted_qty = qty * rate

                    result["v"] = converted_qty 
        else:
            result = {"err": "invalid request"}

        utils.write_jsonp_output(response, result, callback)
