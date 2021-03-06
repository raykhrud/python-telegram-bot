#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2017
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains an object that represents Tests for Telegram Venue"""

import sys
import unittest

from flaky import flaky

sys.path.append('.')

import telegram
from tests.base import BaseTest


class VenueTest(BaseTest, unittest.TestCase):
    """This object represents Tests for Telegram Venue."""

    def setUp(self):
        self.location = telegram.Location(longitude=-46.788279, latitude=-23.691288)
        self.title = 'title'
        self._address = '_address'
        self.foursquare_id = 'foursquare id'

        self.json_dict = {
            'location': self.location.to_dict(),
            'title': self.title,
            'address': self._address,
            'foursquare_id': self.foursquare_id
        }

    def test_venue_de_json(self):
        sticker = telegram.Venue.de_json(self.json_dict, self._bot)

        self.assertTrue(isinstance(sticker.location, telegram.Location))
        self.assertEqual(sticker.title, self.title)
        self.assertEqual(sticker.address, self._address)
        self.assertEqual(sticker.foursquare_id, self.foursquare_id)

    def test_send_venue_with_venue(self):
        ven = telegram.Venue.de_json(self.json_dict, self._bot)
        message = self._bot.send_venue(chat_id=self._chat_id, venue=ven)
        venue = message.venue

        self.assertEqual(venue, ven)

    def test_venue_to_json(self):
        sticker = telegram.Venue.de_json(self.json_dict, self._bot)

        self.assertTrue(self.is_json(sticker.to_json()))

    def test_sticker_to_dict(self):
        sticker = telegram.Venue.de_json(self.json_dict, self._bot).to_dict()

        self.assertTrue(self.is_dict(sticker))
        self.assertDictEqual(self.json_dict, sticker)

    @flaky(3, 1)
    def test_reply_venue(self):
        """Test for Message.reply_venue"""
        message = self._bot.sendMessage(self._chat_id, '.')
        message = message.reply_venue(self.location.latitude, self.location.longitude, self.title,
                                      self._address)

        self.assertAlmostEqual(message.venue.location.latitude, self.location.latitude, 2)
        self.assertAlmostEqual(message.venue.location.longitude, self.location.longitude, 2)

    def test_equality(self):
        a = telegram.Venue(telegram.Location(0, 0), "Title", "Address")
        b = telegram.Venue(telegram.Location(0, 0), "Title", "Address")
        c = telegram.Venue(telegram.Location(0, 0), "Title", "Not Address")
        d = telegram.Venue(telegram.Location(0, 1), "Title", "Address")
        d2 = telegram.Venue(telegram.Location(0, 0), "Not Title", "Address")

        self.assertEqual(a, b)
        self.assertEqual(hash(a), hash(b))
        self.assertIsNot(a, b)

        self.assertEqual(a, c)
        self.assertEqual(hash(a), hash(c))

        self.assertNotEqual(a, d)
        self.assertNotEqual(hash(a), hash(d))

        self.assertNotEqual(a, d2)
        self.assertNotEqual(hash(a), hash(d2))


if __name__ == '__main__':
    unittest.main()
