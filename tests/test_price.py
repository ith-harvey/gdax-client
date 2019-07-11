# This file is part of Maker Keeper Framework.
#
# Copyright (C) 2017-2018 reverendus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import time

import pytest
from decimal import *

from gdax_client.price import GdaxPriceClient, GDAX_WS_URL

@pytest.fixture
def _init_price_feed():
    price_client = GdaxPriceClient(GDAX_WS_URL, "ETH-USD", 120)

    # provides time for feed to initiate
    time.sleep(1)

    return price_client

@pytest.fixture
def _build_update(side, price, amount):
    return {
            'type': 'l2update',
            'product_id': 'ETH-USD',
            'time': '2019-07-11T19:35:08.072Z',
            'changes': [[side, price, amount]]
            }

@pytest.fixture
def _seed_l2update(price_client):

    fake_l2update = _build_update('sell', '273.31000000', '2')

    price_client._process_l2update(fake_l2update)

    return

def test_obook_price_feed():

    price_client = _init_price_feed()

    assert type(price_client.get_obook_price()) is Decimal


def test_obook_l2update_updating():

    price_client = _init_price_feed()
    _seed_l2update(price_client)

    assert price_client._asks.get(Decimal('273.31000000')) == Decimal('2')

def test_obook_l2update_removing():

    price_client = _init_price_feed()
    _seed_l2update(price_client)
    remove_l2update = _build_update('sell', '273.31000000', '0')
    price_client._process_l2update(remove_l2update)

    assert price_client._asks.__contains__(Decimal('273.31000000')) == False

def test_obook_asks():

    price_client = _init_price_feed()
    best_ask = price_client._asks.peekitem(0)[0]
    second_best_ask = price_client._asks.peekitem(1)[0]

    assert best_ask < second_best_ask

def test_obook_bids():

    price_client = _init_price_feed()
    best_bid = price_client._bids.peekitem(0)[0]
    second_best_bid = price_client._bids.peekitem(1)[0]

    assert best_bid > second_best_bid

def test_obook_no_cross():

    price_client = _init_price_feed()
    best_bid = price_client._bids.peekitem(0)[0]
    best_ask = price_client._asks.peekitem(0)[0]

    assert best_ask > best_bid

def test_gdax_ticker_price_feed():

    price_client = _init_price_feed()

    assert type(price_client.get_price()) is Decimal
