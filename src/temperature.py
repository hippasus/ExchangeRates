#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2, json, utils

invalid_request = {"err": "invalid request."}

def convert_temperature(mode, qty):
    if utils.is_none_or_empty(mode):
        return None

    mode_upper = mode.upper()

    if mode_upper == 'C2F': # Celsius to Fahrenheit
        v = qty * 9.0 / 5.0 + 32
    elif mode_upper == 'F2C':
        v = (qty -  32) * 5.0 / 9.0

    return v

class Temperature(webapp2.RequestHandler):
    def get(self):
        request, response = self.request, self.response

        mode, qty_str, jsonp_callback = request.get('mode'), request.get('q'), request.get('callback')

        try:
            qty = float(qty_str)
        except Exception, e:
            qty = None

        converted = None
        if not utils.is_none(qty):
            converted = convert_temperature(mode, qty)

        if not utils.is_none(converted):
            result = {"mode": mode, "qty": qty, "v": converted }
        else:
            result = invalid_request

        utils.write_jsonp_output(response, result, jsonp_callback)

