#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import webapp2, currency_rates

class Main(webapp2.RequestHandler):
    def get(self):
        html = """
<!DOCTYPE html>
<html dir="ltr">
    <head>
        <meta charset="utf-8">
        <title i18n-content="title">New Tab</title>
        <style>
            body { font: 1.2em/1.2 Arial; }
            h1 { font: bold 2em/2 Verdana; }
            p { padding: 10px 20px; font: 1em/1.5 Consolas; color: #bdbdbd; text-align: right; }
        </style>
    </head>
    <body>
        <h1>Rate Exchange</h1>
        <ul>
            <li>Currency: <a href="/currency?from=USD&to=EUR&q=1" target="_blank" rel="nofollow">/currency?from=USD&to=EUR&q=1</a></li>
        </ul>
        <p>--By Hippasus Chu</p>
    </body>
</html>
        """
        
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(html)

app = webapp2.WSGIApplication([
                               ('/', Main),
                               ('/currency', currency_rates.CurrencyRates)])
