#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2, currency_rates, temperature

class Main(webapp2.RequestHandler):
    def get(self):
        html = """
<!DOCTYPE html>
<html dir="ltr">
    <head>
        <meta charset="utf-8">
        <title>Rate Exchange JSON/JSONP APIs by Hippasus Chu</title>
        <style>
            body { font: 1.2em/1.2 Arial; }
            h1 { font: bold 2em/2 Verdana; }
            p { padding: 10px 20px; font: 1em/1.5 Consolas; color: #bdbdbd; text-align: right; }
        </style>
    </head>
    <body>
        <h1>Rate Exchange JSON/JSONP APIs</h1>
        <ul>
            <li>Currency API: <a href="$host_url/currency?from=USD&to=EUR&q=1" target="_blank" rel="nofollow">$host_url/currency?from=USD&to=EUR&q=1</a></li>
            <li>Temperature API: <a href="$host_url/temperature?mode=C2F&q=37" target="_blank" rel="nofollow">$host_url/temperature?mode=C2F&q=37</a></li>
        </ul>
        <div>
            Got an error? Please help to create issue at <a href="https://github.com/hippasus/ExchangeRates/issues">https://github.com/hippasus/ExchangeRates/issues</a>.
        </div>
        <p>--By Hippasus Chu</p>
    </body>
</html>
        """
        
        html = html.replace('$host_url', self.request.host_url)
        
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(html)

app = webapp2.WSGIApplication([
                               ('/', Main),
                               ('/currency', currency_rates.CurrencyRates),
                               ('/temperature', temperature.Temperature)])
