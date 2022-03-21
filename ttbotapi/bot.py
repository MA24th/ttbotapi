# -*- coding: utf-8 -*-

"""
ttbotapi.bot
~~~~~~~~~~~~
:copyright: (c) 2022 by Mustafa Asaad.
:license: GPLv2, see LICENSE for more details.
"""
from . import methods
from . import objects


class Bot:
    def __init__(self, access_token, proxies=None):
        """
        Use this class to create a bot instance
        :param str access_token: Bot token gain by @PrimeBot
        :param dict or None proxies: Dictionary mapping protocol to the URL of the proxy
        """
        self.__access_token = access_token
        self.__proxies = proxies

    def get_bot_info(self):
        """
        Get info about current bot
        :return: On Success, a User object
        :rtype: objects.User
        """
        resp = methods.get_bot_info(self.__access_token, self.__proxies)
        return objects.User.de_json(resp)

    def edit_bot_info(self, name=None, username=None, description=None, commands=None, photo=None):
        """
        Edits current bot info,
        Fill only the fields you want to update,
        All remaining fields will stay untouched
        :param str or None name: Visible name of bot
        :param str or None username: Bot unique identifier
        :param str or None description: Bot description up to 16k characters long
        :param list[objects.BotCommand] or None commands: Commands supported by bot, Pass empty list to remove commands
        :param any photo: Request to set bot photo
        :return: On Success, a User object
        :rtype: objects.User
        """
        resp = methods.edit_bot_info(self.__access_token, name, username, description, commands, photo, self.__proxies)
        return objects.User.de_json(resp)

    def get_all_chats(self, count=50, marker=None):
        """
        Get information about chats that bot participated in
        :param int or None count: Number of chats requested
        :param int or None marker: Points to Next data page
        :return: On Success, Array of Chat Object
        :rtype: list[objects.Chat]
        """
        resp = methods.get_all_chats(self.__access_token, count, marker, self.__proxies)
        chats = []
        for x in resp['chats']:
            chats.append(objects.Chat.de_json(x))
        return chats

    def get_chat_by_link(self, chat_link):
        """
        Get chat/channel information by its public link or dialog with user by username
        :param str chat_link: Public chat link or username
        :return: On Success, a Chat Object
        :rtype: objects.Chat
        """
        resp = methods.get_chat_by_link(self.__access_token, chat_link, self.__proxies)
        return objects.Chat.de_json(resp)

    def get_chat(self, chat_link):
        """
        Get info about chat
        :param chat_link: Requested chat identifier
        :return: On Success, a Chat Object
        :rtype: objects.Chat
        """
        resp = methods.get_chat(self.__access_token, chat_link, self.__proxies)
        return objects.Chat.de_json(resp)

    def edit_chat_info(self, chat_id, icon=None, title=None, pin=None, notify=True):
        """
        Edit chat info
        :param int chat_id: chat identifier
        :param any icon: Request to attach image
        :param str or None title: chat title
        :param str or None pin: Identifier of message to be pinned in chat
        :param bool notify: By default, participants will be notified about change with system message in chat/channel
        :return: On Success, a Chat Object
        :rtype: objects.Chat
        """
        resp = methods.edit_chat_info(self.__access_token, chat_id, icon, title, pin, notify, self.__proxies)
        return objects.Chat.de_json(resp)

    def send_action(self, chat_id, action):
        """
        Send bot action to chat
        :param int chat_id: chat identifier
        :param str action: Enum: "typing_on" "sending_photo" "sending_video" "sending_audio" "sending_file" "mark_seen"
                             Different actions to send to chat members
        :return: On success, True
        :rtype: dict
        """
        resp = methods.send_action(self.__access_token, chat_id, action, self.__proxies)
        return resp

    def get_pinned_message(self, chat_id):
        """
        Get pinned message in chat or channel
        :param int chat_id: chat identifier
        :return: On success, a Message Object
        :rtype: objects.Message
        """
        resp = methods.get_pinned_message(self.__access_token, chat_id, self.__proxies)
        if resp:
            return objects.Message.de_json(resp['message'])
        return resp

    def pin_message(self, chat_id, message_id, notify=True):
        """
        Pins message in chat or channel
        :param int chat_id: chat identifier
        :param str message_id: Identifier of message to be pinned in chat
        :param bool notify: By default, participants will be notified about change with system message in chat/channel
        :return: True, On success
        :rtype: dict
        """
        resp = methods.pin_message(self.__access_token, chat_id, message_id, notify, self.__proxies)
        return resp

    def unpin_message(self, chat_id):
        """
        Unpins message in chat or channel
        :param int chat_id: chat identifier
        :return: True, On success
        :rtype: dict
        """
        resp = methods.unpin_message(self.__access_token, chat_id, self.__proxies)
        return resp

    def get_chat_membership(self, chat_id):
        """
        Get chat membership info for current bot
        :param int chat_id: chat identifier
        :return: User Object, On success
        :rtype: objects.User
        """
        resp = methods.get_chat_membership(self.__access_token, chat_id, self.__proxies)
        return objects.User.de_json(resp)

    def leave_chat(self, chat_id):
        """
        Removes bot from chat members
        :param int chat_id: chat identifier
        :return: True, On success
        :rtype: dict
        """
        resp = methods.leave_chat(self.__access_token, chat_id, self.__proxies)
        return resp

    def get_chat_admins(self, chat_id):
        """
        Get all chat administrator, Bot must be administrator in requested chat
        :param int chat_id: chat identifier
        :return: Array of Users, On success
        :rtype: list[objects.User]
        """
        resp = methods.get_chat_admins(self.__access_token, chat_id, self.__proxies)
        users = []
        for x in resp['members']:
            users.append(objects.User.de_json(x))
        return users

    def get_chat_members(self, chat_id, user_ids=None, marker=None, count=20):
        """
        Get users participated in chat
        :param int chat_id: chat identifier
        :param list[int] or None user_ids: users identifier
        :param int or None marker: a Marker
        :param int count: Default 20, Count
        :return: Array of Users, On success
        :rtype: list[objects.User]
        """
        resp = methods.get_members(self.__access_token, chat_id, user_ids, marker, count, self.__proxies)
        users = []
        for x in resp['members']:
            users.append(objects.User.de_json(x))
        return users

    def add_members(self, chat_id, user_ids):
        """
        Adds members to chat
        :param int chat_id: chat identifier
        :param list[int] user_ids: users identifier
        :return: True, On success
        :rtype: dict
        """
        resp = methods.add_members(self.__access_token, chat_id, user_ids, self.__proxies)
        return resp

    def remove_member(self, chat_id, user_ids, block=False):
        """
        Removes member for chat
        :param chat_id: chat identifier
        :param user_ids: users identifier
        :param block: Set to True if user should be blocked in chat
        :return: True, On success
        :rtype: dict
        """
        resp = methods.remove_member(self.__access_token, chat_id, user_ids, block, self.__proxies)
        return resp

    def get_messages(self, chat_id=None, message_ids=None, ffrom=None, to=None, count=50):
        """
        Get messages in chat
        :param int or None chat_id: Chat identifier
        :param int or None message_ids: Messages identifier
        :param int or None ffrom: Start time for requested messages
        :param int or None to: End time for requested messages
        :param int count:
        :return: On Success, Array of Messages
        :rtype: list[objects.Message]
        """
        resp = methods.get_messages(self.__access_token, chat_id, message_ids, ffrom, to, count, self.__proxies)
        messages = []
        for x in resp:
            messages.append(objects.Message.de_json(x))
        return messages

    def send_message(self, text, chat_id, user_id, attachments=None, link=None, formatter=None, notify=True,
                     disable_link_preview=False):
        """
        Send a message to chat
        :param str text: Message text
        :param int or None chat_id: Fill this if you send message to chat
        :param int or None user_id: Fill this parameter if you want to send message to user
        :param list[object] attachments: Message attachments
        :param object or None link: Link to Message
        :param str or None formatter: Enum: "markdown" "html" If set, message text will be formatted
        :param bool notify: If false, chat participants would not be notified
        :param bool disable_link_preview: If false, server will not generate media preview for links in text
        :return: On Success, a Message object
        :rtype: objects.Message
        """
        resp = methods.send_message(self.__access_token, user_id, chat_id, disable_link_preview, text, attachments,
                                    link, notify, formatter, self.__proxies)
        return objects.Message.de_json(resp)

    def edit_message(self, message_id, text, attachments=None, link=None, notify=True, formatter=None):
        """
        Edit existing message
        :param str message_id: Message identifier
        :param str text: Message text
        :param list[object] or None attachments: Message attachments
        :param str or None link: Link to message
        :param bool notify: If false, chat participants would not be notified
        :param str or None formatter: Enum: "markdown" "html" If set, message text will be formatted
        :return: True, On success
        :rtype: dict
        """
        resp = methods.edit_message(self.__access_token, message_id, text, attachments, link, notify, formatter,
                                    self.__proxies)
        return resp

    def delete_message(self, message_id):
        """
        Delete existing message
        :param str message_id: Message identifier
        :return: True, On success
        :rtype: dict
        """
        resp = methods.delete_message(self.__access_token, message_id, self.__proxies)
        return resp

    def get_message(self, message_id):
        """
        Get existing message
        :param str message_id: Message identifier
        :return: On Success, a Message Object
        :rtype: objects.Message
        """
        resp = methods.get_message(self.__access_token, message_id, self.__proxies)
        return objects.Message.de_json(resp)

    def answer_on_callback(self, callback_id, message=None, notification=False):
        """
        This method should be called to send an answer after a user has clicked the button
        :param str callback_id: Identifies a button clicked by user
        :param message: Fill this if you want to modify current message
        :param notification: Fill this if you want to send one time notification to user
        :return: True, On success
        :rtype: dict
        """
        resp = methods.answer_on_callback(self.__access_token, callback_id, message, notification, self.__proxies)
        return resp

    def construct_message(self, session_id, messages=None, allow_user_input=False, hint=None, data=None, keyboard=None,
                          placeholder=None):
        """
        Sends answer on construction request
        :param str session_id: Constructor session identifier
        :param list[object] or None messages: Array of prepared messages
        :param bool allow_user_input: If true user can send any input manually Otherwise, only keyboard will be shown
        :param str or None hint: Hint to user. Will be shown on top of keyboard
        :param str or None data: In this property you can store any additional data up to 8KB,
                                 We send this data back to bot within the next construction request,
                                 It is handy to store here any state of construction session
        :param object or None keyboard: Keyboard to show to user in constructor mode
        :param str or None placeholder: Text to show over the text field
        :return: True, On success
        :rtype: dict
        """
        resp = methods.construct_message(self.__access_token, session_id, messages, allow_user_input, hint, data,
                                         keyboard, placeholder, self.__proxies)
        return resp

    def get_subscriptions(self):
        """
        In case your bot gets data via WebHook, the method returns list of all subscriptions
        :return: On Success, Array of Subscriptions object
        :rtype: list[object]
        """
        resp = methods.get_subscriptions(self.__access_token, self.__proxies)
        return resp

    def subscribe(self, url, update_types=None, version=None):
        """
        Subscribes bot to receive updates via WebHook
        :param str url: URL of HTTP(S)-endpoint of your bot. Must starts with http(s)://
        :param list[str] or None update_types: List of update types your bot want to receive
        :param str or None version: Version of API, Affects model representation
        :return: True, On success
        :rtype: dict
        """
        resp = methods.subscribe(self.__proxies, url, update_types, version, self.__proxies)
        return resp

    def unsubscribe(self, url):
        """
        Unsubscribes bot from receiving updates via WebHook
        :param str url:
        :return: True, On success
        :rtype: dict
        """
        resp = methods.unsubscribe(self.__access_token, url, self.__proxies)
        return resp

    def get_updates(self, limit=100, timeout=30, marker=None, types=None):
        """
        You can use this method for getting updates in case your bot is not subscribed to WebHook,
        The method is based on long polling
        :param int limit: Maximum number of updates to be retrieved
        :param int timeout: Timeout in seconds for long polling
        :param int marker: Pass None to get updates you didn't get yet
        :param list[str] or None types: Comma separated list of update types your bot want to receive
        :return: On Success, Array of Update object
        :rtype: list[objects.Update]
        """
        resp = methods.get_update(self.__access_token, limit, timeout, marker, types, self.__proxies)
        updates = []
        for x in resp['updates']:
            updates.append(objects.Update.de_json(x))
        return updates

    def get_upload_url(self, data, ttype):
        """
        Returns the URL for the subsequent file upload
        :param any data: file to be uploaded
        :param ttype: type of the file
        :return: On Success, Url of uploaded file
        :rtype: str
        """
        resp = methods.get_upload_url(self.__access_token, data, ttype, self.__proxies)
        return resp
