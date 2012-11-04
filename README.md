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

<table>
    <thead>
        <tr>
            <th>Request</th>
            <th>Response</th>
        </tr>
    </thead>
    <tbody>
        <tr><td><code>/currency?from=USD&to=EUR</code></td><td><code>{"to": "EUR", "rate": 0.77966630299999995, "from": "USD"}</code></td></tr>
        <tr><td><code>/currency?from=USD&to=EUR&q=2</code></td><td><code>{"to": "EUR", "rate": 0.77966630299999995, "from": "USD", "v": 1.5593326059999999}</code></td></tr>
        <tr><td><code>/currency?from=USD&to=EUR&callback=jsonpCallback</code></td><td><code>jsonpCallback({"to": "EUR", "rate": 0.77966630299999995, "from": "USD"})</code></td></tr>
        <tr><td><code>/currency?from=USD&to=EUR&q=2&callback=jsonpCallback</code></td><td><code>jsonpCallback({"to": "EUR", "rate": 0.77966630299999995, "from": "USD", "v": 1.5593326059999999})</code></td></tr>
        <tr><td><code>/currency?from=USD</code></td><td><code>{"err": "invalid request"}</code></td></tr>
    </tbody>
</table>

### Temperature API

By invoking the temperature API, send a request to `/temperature` as follows:

    /temperature?mode=C2F&q=37

The mode can be `C2F`(Celsius to Fahrenheit) or `F2C`(Fahrenheit to Celsius). A jsonp `callback` parameter is optional. The response is as:

    {"v": 98.6, "mode": "C2F", "qty": 37.0}

