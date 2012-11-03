#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import json, re, urllib2
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

        def write_output(out_result, jsonp_callback):
            output, content_type = json.dumps(out_result), "application/json"
            
            if (jsonp_callback):
                output = jsonp_callback + "(" + output + ")"
                content_type = 'application/x-javascript'

            response.headers['Content-Type'] = content_type
            response.out.write(output)

        from_currency, to_currency, qty, callback = get_request_params()

        if (from_currency is not None and
            to_currency is not None and
            len(from_currency) > 0 and
            len(to_currency) > 0):
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

        write_output(result, callback)
