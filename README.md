Rate Exchange JSON/JSONP APIs
=============================

This is the rate exchange JSON/JSONP APIs project which is deployed at http://rate-exchange.appspot.com/.

Currently only currency rate exchange is supported.

Usage
----

### Currency API

By invoking the currency API, just send a request to `/currency` as follow:

    /currency?from=USD&to=EUR&q=1&callback=jsonpCallback

And note that the parameter `q` and `callback` is optional.

Here are some samples:

| Request |Response|
|---------|--------|
| `/currency?from=USD&to=EUR` | <code>{<br />&nbsp;&nbsp;&nbsp;&nbsp;"to": "EUR",<br />&nbsp;&nbsp;&nbsp;&nbsp;"rate": 0.77966630299999995,<br />&nbsp;&nbsp;&nbsp;&nbsp;"from": "USD"<br />}</code> |
| `/currency?from=USD&to=EUR&q=2` | <code>{<br />&nbsp;&nbsp;&nbsp;&nbsp;"to": "EUR",<br />&nbsp;&nbsp;&nbsp;&nbsp;"rate": 0.77966630299999995,<br />&nbsp;&nbsp;&nbsp;&nbsp;"from": "USD",<br />&nbsp;&nbsp;&nbsp;&nbsp;"v": 1.5593326059999999}</code> |
| `/currency?from=USD&to=EUR&callback=jsonpCallback` | <code>jsonpCallback({<br />&nbsp;&nbsp;&nbsp;&nbsp;"to": "EUR",<br />&nbsp;&nbsp;&nbsp;&nbsp;"rate": 0.77966630299999995,<br />&nbsp;&nbsp;&nbsp;&nbsp;"from": "USD"<br />})</code> |
| `/currency?from=USD&to=EUR&q=2&callback=jsonpCallback` | <code>jsonpCallback({<br />&nbsp;&nbsp;&nbsp;&nbsp;"to": "EUR",<br />&nbsp;&nbsp;&nbsp;&nbsp;"rate": 0.77966630299999995,<br />&nbsp;&nbsp;&nbsp;&nbsp;"from": "USD",<br />&nbsp;&nbsp;&nbsp;&nbsp;"v": 1.5593326059999999<br />})</code> |
| `/currency?from=USD` | <code>{<br />&nbsp;&nbsp;&nbsp;&nbsp;"err": "invalid request"<br />}</code> |

### Temperature API

By invoking the temperature API, send a request to `/temperature` as follows:

    /temperature?mode=C2F&q=37

The mode can be `C2F`(Celsius to Fahrenheit) or `F2C`(Fahrenheit to Celsius). A jsonp `callback` parameter is optional. The response is as:

    {"v": 98.6, "mode": "C2F", "qty": 37.0}

