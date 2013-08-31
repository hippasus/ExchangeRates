#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2, currency_rates, temperature, logging

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
            p.author { padding: 10px 20px; font: 1em/1.5 Consolas; color: #bdbdbd; text-align: right; }
            .got-error { font-size: 1em; font-family: Verdana; }
        </style>
    </head>
    <body>
        <h1>Rate Exchange JSON/JSONP APIs</h1>
        <ul>
            <li>Currency API: <a href="$host_url/currency?from=USD&to=EUR&q=1" target="_blank" rel="nofollow">$host_url/currency?from=USD&to=EUR&q=1</a></li>
            <li>Temperature API: <a href="$host_url/temperature?mode=C2F&q=37" target="_blank" rel="nofollow">$host_url/temperature?mode=C2F&q=37</a></li>
        </ul>
        <div class="got-error">
            <i>Got an error?</i> Please help to create an issue at <a href="https://github.com/hippasus/ExchangeRates/issues">https://github.com/hippasus/ExchangeRates/issues</a>.
        </div>
        <h3>Help needed!</h3>
        <p>We've reached the <a href="https://developers.google.com/appengine/docs/quotas#UrlFetch" target="_blank">GAE URL Fetch Quota</a> for the currency API.
        <br />And I need your help to enable billing to get larger quota. Do please help to click <a href="http://ko-fi.com?i=8d071856392d304" target="_blank">this link</a> and donate me $1.00USD.</p>
        <p class="author">--By Hippasus Chu</p>

        <script>
            (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
            (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
            m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
            })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

            ga('create', 'UA-43673035-1', 'rate-exchange.appspot.com');
            ga('send', 'pageview');
        </script>
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