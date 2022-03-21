# -*- coding: utf-8 -*-

"""
tests.test_objects
~~~~~~~~~~~~~~~~~~
This submodule provides tests for a TamTam Available objects.
:copyright: (c) 2022 by Mustafa Asaad.
:license: GPLv2, see LICENSE for more details.
"""

import unittest
from ttbotapi.objects import *


class TestUser(unittest.TestCase):
    with open("schema/User.json") as f:
        data = f.read()
    object = User.de_json(data)

    def test_user(self):
        user = self.object
        self.assertEqual(user.user_id, 0)
        self.assertEqual(user.name, "string")
        self.assertEqual(user.username, "string")
        self.assertEqual(user.is_bot, True)
        self.assertEqual(user.last_activity_time, 0)
        self.assertEqual(user.description, "string")
        self.assertEqual(user.avatar_url, "string")
        self.assertEqual(user.full_avatar_url, "string")


class TestChat(unittest.TestCase):
    with open("schema/Chat.json") as f:
        data = f.read()
    object = Chat.de_json(data)

    def test_chat(self):
        chat = self.object
        self.assertEqual(chat.chat_id, 0)


if __name__ == '__main__':
    unittest.main()
