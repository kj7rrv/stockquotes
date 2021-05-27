`stockquotes` is a simple Python module for collecting stock/ETF and mutual fund (see #2)quotes and
historical data from Yahoo! Finance. It's perfect for developers who can't
afford the (often high) prices charged by many stock data APIs.

# Requirements
* Python 3.5+
* Beautiful Soup 4

# Installation

    pip3 install stockquotes

# Usage
First, import the `stockquotes` module.

    import stockquotes

To get a stock quote, instantiate a `stockquotes.Stock` object. The only
parameter is the ticker symbol to look up.

    kroger = stockquotes.Stock('KR')

## Basic data
To get the current price of a share, get the `Stock`'s `current_price`.

    kroger_price = kroger.current_price

To get the day gain in dollars, get the `Stock`'s `increase_dollars`.

    kroger_gain_dollars = kroger.increase_dollars

The same value as a percent is available in the `increase_percent` property. To
indicate losses, these values are negative.

## Historical data
The historical data for a stock can be accessed through the `Stock`'s
`historical` property. This is an array of `dict`s, with the first item
representing the most recent quote. The `dict`'s `date` property is a
`datetime` object representing the date the quote is from. `open` is the
opening price for that day. `high` and `low` are the high and low prices,
respectively, for that day. `close` and `adjusted_close` are the closing
price. The difference is that `adjClose` is adjusted for splits and
dividends, whereas `close` is adjusted only for splits. `volume` is the
stock's volume for that day.

Typically, this should give at least a month of data. Obviously, it gives less
for recent IPOs. Also, a known but unexplained bug causes it to only give two
days of data for some stocks.

# Exceptions
`stockquotes.StockDoesNotExistError` is raised when the stock does not exist.

`stockquotes.NetworkError` is raised when a connection to Yahoo! Finance
cannot be established.

# License
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org/>
