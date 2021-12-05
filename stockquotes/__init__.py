#!/usr/bin/env python3
# stockquotes - Python module to pull stock quotes from Yahoo! Finance
# Copyright 2020 ScoopGracie. All rights reversed.
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from bs4 import BeautifulSoup as bs
import requests
import datetime


class StockDoesNotExistError(Exception):
    pass


class NetworkError(Exception):
    pass


class Stock:
    def __init__(self, ticker):
        try:
            r = requests.get(
                "https://finance.yahoo.com/quote/{}/history".format(ticker),
                headers={
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3941.4 Safari/537.36"
                },
            )
        except:
            raise NetworkError()
        if r.status_code == 302:
            raise StockDoesNotExistError(ticker)
        try:
            soup = bs(r.text, features="lxml")
            self.symbol = soup.h1.string.split("(")[1].split(")")[0]
            self.name = soup.h1.string.split("(")[0].strip()
            rows = soup.table.tbody.find_all("tr")
            self.historical = []
            for i in rows:
                row = i.find_all("td")
                try:
                    parsed = {
                        "date": datetime.datetime.strptime(
                            row[0].span.string, "%b %d, %Y"
                        ),
                        "open": float(row[1].span.string.replace(",", "")),
                        "high": float(row[2].span.string.replace(",", "")),
                        "low": float(row[3].span.string.replace(",", "")),
                        "close": float(row[4].span.string.replace(",", "")),
                        "adjusted_close": float(
                            row[5].span.string.replace(",", "")
                        ),
                        "volume": int(row[6].span.string.replace(",", ""))
                        if row[6].string != "-"
                        else None,
                    }
                except:
                    continue

                self.historical.append(parsed)

            price_selector = f'fin-streamer[data-field="regularMarketPrice"][data-symbol="{self.symbol}"]'
            price_element = soup.select_one(price_selector)
            self.current_price = float(price_element.text)

            change_selector = f'fin-streamer[data-field="regularMarketChange"][data-symbol="{self.symbol}"]'
            change_element = soup.select_one(change_selector)
            self.increase_dollars = float(change_element.text)

            change_percent_selector = f'fin-streamer[data-field="regularMarketChangePercent"][data-symbol="{self.symbol}"]'
            change_percent_element = soup.select_one(change_percent_selector)
            change_percent_text = ''.join([char for char in change_percent_element.text if char in '-.0123456789'])
            self.increase_percent = float(change_percent_text)
        except AttributeError as error:
            raise StockDoesNotExistError(ticker) from error
