#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import json

def is_none(target):
    return target is None

def is_none_or_empty(target):
    return is_none(target) or len(target) == 0

def write_json_output(response, dic):
    response_text, content_type = json.dumps(dic), "application/json"
    _do_write(response, response_text, content_type)

def write_jsonp_output(response, dic, jsonp_callback):
    if is_none_or_empty(jsonp_callback):
        write_json_output(response, dic)
    else:
        response_text, content_type = jsonp_callback + "(" + json.dumps(dic) + ")", "application/x-javascript"
        _do_write(response, response_text, content_type)

def _do_write(response, response_text, content_type):
    response.headers['Content-Type'] = content_type
    response.out.write(response_text)