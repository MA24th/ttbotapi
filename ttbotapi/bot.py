# -*- coding: utf-8 -*-

"""
ttbotapi.bot
~~~~~~~~~~~~
:copyright: (c) 2022 by Mustafa Asaad.
:license: GPLv2, see LICENSE for more details.
"""
import threading
import time
import re

from . import utils
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

        self.__stop_polling = threading.Event()

        self.__last_marker = 0

        self.__message_callback_handlers = []
        self.__message_created_handlers = []
        self.__message_removed_handlers = []
        self.__message_edited_handlers = []
        self.__bot_added_handlers = []
        self.__bot_removed_handlers = []
        self.__user_added_handlers = []
        self.__user_removed_handlers = []
        self.__bot_started_handlers = []
        self.__chat_title_changed_handlers = []
        self.__message_construction_request_handlers = []
        self.__message_constructed_handlers = []
        self.__message_chat_created_handlers = []

    def update_handler(self, update_type='message_created', chat_type=None, bot_command=None, regexp=None, func=None):
        """
        Update handler decorator
        :param str or list update_type: specify one of allowed_updates to take action
        :param str or list or None chat_type: list of chat types (dialog, chat, channel)
        :param str or list or None bot_command: Bot Commands like (/start, /help)
        :param str or None regexp: Sequence of characters that define a search pattern
        :param function or None func: any python function that return True On success like (lambda)
        :return: filtered Update`
        """

        def decorator(handler):
            if 'message_callback' in update_type:
                self.__message_callback_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                                  bot_command=bot_command,
                                                                                  regexp=regexp, func=func))
            elif 'message_created' in update_type:
                self.__message_created_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                                 bot_command=bot_command,
                                                                                 regexp=regexp, func=func))
            elif 'message_removed' in update_type:
                self.__message_removed_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                                 bot_command=bot_command,
                                                                                 regexp=regexp, func=func))
            elif 'message_edited' in update_type:
                self.__message_edited_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                                bot_command=bot_command,
                                                                                regexp=regexp, func=func))
            elif 'bot_added' in update_type:
                self.__bot_added_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                           bot_command=bot_command,
                                                                           regexp=regexp, func=func))
            elif 'bot_removed' in update_type:
                self.__bot_removed_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                             bot_command=bot_command,
                                                                             regexp=regexp, func=func))
            elif 'user_added' in update_type:
                self.__user_added_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                            bot_command=bot_command,
                                                                            regexp=regexp, func=func))
            elif 'user_removed' in update_type:
                self.__user_removed_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                              bot_command=bot_command,
                                                                              regexp=regexp, func=func))
            elif 'bot_started' in update_type:
                self.__bot_started_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                             bot_command=bot_command,
                                                                             regexp=regexp, func=func))
            elif 'chat_title_changed' in update_type:
                self.__chat_title_changed_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                                    bot_command=bot_command,
                                                                                    regexp=regexp, func=func))
            elif 'message_construction_request' in update_type:
                self.__message_construction_request_handlers.append(
                    self.__build_handler_dict(handler, chat_type=chat_type,
                                              bot_command=bot_command,
                                              regexp=regexp, func=func))
            elif 'message_constructed' in update_type:
                self.__message_constructed_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                                     bot_command=bot_command,
                                                                                     regexp=regexp, func=func))
            elif 'message_chat_created' in update_type:
                self.__message_chat_created_handlers.append(self.__build_handler_dict(handler, chat_type=chat_type,
                                                                                      bot_command=bot_command,
                                                                                      regexp=regexp, func=func))
            return handler

        return decorator

    @staticmethod
    def __build_handler_dict(handler, **filters):
        """
        Builds a dictionary for a handler
        :param handler: functions name
        :param filters: functions filters
        :return: Return Dictionary type for handlers
        :rtype: dict
        """
        return {
            'function': handler,
            'filters': filters
        }

    def polling(self, none_stop=False, limit=100, timeout=30, types=None):
        """
        This function creates a new Thread that calls an internal __retrieve_updates function
        This allows the bot to retrieve Updates automatically and notify listeners and message handlers accordingly
        Warning: Do not call this function more than once!
        Always get updates
        :param bool none_stop: Do not stop polling when an ApiException occurs
        :param limit:
        :param int timeout: Timeout in seconds for long polling
        :param types:
        :return:
        """
        interval = 0
        error_interval = 0.25
        utils.logger.info('POLLING STARTED')

        while not self.__stop_polling.wait(interval):
            try:
                self.__retrieve_updates(limit, timeout, types)
            except utils.ApiException as e:
                utils.logger.error(e)
                if not none_stop:
                    self.__stop_polling.set()
                    utils.logger.info("Exception Occurred, POLLING STOPPED")
                else:
                    utils.logger.info(f"Waiting for {error_interval} seconds until retry")
                    time.sleep(error_interval)
                    error_interval *= 2
            except KeyboardInterrupt:
                utils.logger.info("KeyboardInterrupt Occurred")
                self.__stop_polling.set()
                utils.logger.info('POLLING STOPPED')
                break

    def __retrieve_updates(self, limit, timeout, types=None):
        """
        Retrieves any updates from the TamTam API
        :return:
        """
        marker = (self.__last_marker + 1)
        updates = self.get_updates(limit, timeout, marker, types)
        self.__process_new_updates(updates)

    def __process_new_updates(self, updates):
        new_message_callback = []
        new_message_created = []
        new_message_removed = []
        new_message_edited = []
        new_bot_added = []
        new_bot_removed = []
        new_user_added = []
        new_user_removed = []
        new_bot_started = []
        new_chat_title_changed = []
        new_message_construction_request = []
        new_message_constructed = []
        new_message_chat_created = []

        if updates.marker > self.__last_marker:
            self.__last_marker = updates.marker
        for update in updates.updates:
            if update.update_type == 'message_callback':
                new_message_callback.append(update)
            if update.update_type == 'message_created':
                new_message_created.append(update)
            if update.update_type == 'message_removed':
                new_message_removed.append(update)
            if update.update_type == 'message_edited':
                new_message_edited.append(update)
            if update.update_type == 'bot_added':
                new_bot_added.append(update)
            if update.update_type == 'bot_removed':
                new_bot_removed.append(update)
            if update.update_type == 'user_added':
                new_user_added.append(update)
            if update.update_type == 'user_removed':
                new_user_removed.append(update)
            if update.update_type == 'bot_started':
                new_bot_started.append(update)
            if update.update_type == 'chat_title_changed':
                new_chat_title_changed.append(update)
            if update.update_type == 'message_construction_request':
                new_message_construction_request.append(update)
            if update.update_type == 'message_constructed':
                new_message_constructed.append(update)
            if update.update_type == 'message_chat_created':
                new_message_chat_created.append(update)

        if len(updates.updates) > 0:
            if len(new_message_callback) > 0:
                self.__process_new_message_callback(new_message_callback)
            if len(new_message_created) > 0:
                self.__process_new_message_created(new_message_created)
            if len(new_message_removed) > 0:
                self.__process_new_message_removed(new_message_removed)
            if len(new_message_edited) > 0:
                self.__process_new_message_edited(new_message_edited)
            if len(new_bot_added) > 0:
                self.__process_new_bot_added(new_bot_added)
            if len(new_bot_removed) > 0:
                self.__process_new_bot_removed(new_bot_removed)
            if len(new_user_added) > 0:
                self.__process_new_user_added(new_user_added)
            if len(new_user_removed) > 0:
                self.__process_new_user_removed(new_user_removed)
            if len(new_bot_started) > 0:
                self.__process_new_bot_started(new_bot_started)
            if len(new_message_construction_request) > 0:
                self.__process_new_message_construction_request(new_message_construction_request)
            if len(new_message_constructed) > 0:
                self.__process_new_message_constructed(new_message_constructed)
            if len(new_message_chat_created) > 0:
                self.__process_new_message_chat_created(new_message_chat_created)

    def __check_update_handler(self, update_handler, update):
        """
        check update handler
        :param update_handler:
        :param update:
        :return:
        """
        for filters, filter_value in update_handler['filters'].items():
            if filter_value is None:
                continue

            if not self.__check_filter(filters, filter_value, update):
                return False

        return True

    @staticmethod
    def __check_filter(filters, filter_value, update):
        """
        check filters
        :param filters:
        :param filter_value:
        :param update:
        :return:
        """
        if filters == 'chat_type':
            return update.message.recipient.chat_type in filter_value
        elif filters == 'regexp':
            return update.message.body.text and re.search(filter_value, update.message.body.text, re.IGNORECASE)
        elif filters == 'func':
            return filter_value(update)
        elif filters == 'bot_command':
            return update.message.body.text in filter_value
        else:
            return False

    @staticmethod
    def __exec_task(task, *args, **kwargs):
        task(*args, **kwargs)

    def __notify_update_handler(self, handlers, new_updates):
        """
        Notifies update handlers
        :param list handlers:
        :param list new_updates:
        :return:
        """
        for update in new_updates:
            for update_handler in handlers:
                if self.__check_update_handler(update_handler, update):
                    self.__exec_task(update_handler['function'], update)
                    break

    def __process_new_message_callback(self, new_message_callback):
        self.__notify_update_handler(self.__message_callback_handlers, new_message_callback)

    def __process_new_message_created(self, new_message_created):
        self.__notify_update_handler(self.__message_created_handlers, new_message_created)

    def __process_new_message_removed(self, new_message_removed):
        self.__notify_update_handler(self.__message_removed_handlers, new_message_removed)

    def __process_new_message_edited(self, new_message_edited):
        self.__notify_update_handler(self.__message_edited_handlers, new_message_edited)

    def __process_new_bot_started(self, new_bot_started):
        self.__notify_update_handler(self.__bot_started_handlers, new_bot_started)

    def __process_new_bot_removed(self, new_bot_removed):
        self.__notify_update_handler(self.__bot_removed_handlers, new_bot_removed)

    def __process_new_user_added(self, new_user_added):
        self.__notify_update_handler(self.__user_added_handlers, new_user_added)

    def __process_new_user_removed(self, new_user_removed):
        self.__notify_update_handler(self.__user_removed_handlers, new_user_removed)

    def __process_new_bot_added(self, new_bot_added):
        self.__notify_update_handler(self.__bot_added_handlers, new_bot_added)

    def __process_new_chat_title_changed(self, new_chat_title_changed):
        self.__notify_update_handler(self.__chat_title_changed_handlers, new_chat_title_changed)

    def __process_new_message_construction_request(self, new_message_construction_request):
        self.__notify_update_handler(self.__message_construction_request_handlers, new_message_construction_request)

    def __process_new_message_constructed(self, new_message_constructed):
        self.__notify_update_handler(self.__message_constructed_handlers, new_message_constructed)

    def __process_new_message_chat_created(self, new_message_chat_created):
        self.__notify_update_handler(self.__message_chat_created_handlers, new_message_chat_created)

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
        :return: On Success, ChatInfo Object
        :rtype: objects.ChatInfo
        """
        resp = methods.get_all_chats(self.__access_token, count, marker, self.__proxies)
        return objects.ChatInfo.de_json(resp)

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
        :return: On success, Response Object
        :rtype: objects.Response
        """
        resp = methods.send_action(self.__access_token, chat_id, action, self.__proxies)
        return objects.Response.de_json(resp)

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
        :return: On success, Response Object
        :rtype: objects.Response
        """
        resp = methods.pin_message(self.__access_token, chat_id, message_id, notify, self.__proxies)
        return objects.Response.de_json(resp)

    def unpin_message(self, chat_id):
        """
        Unpins message in chat or channel
        :param int chat_id: chat identifier
        :return: On success, Response Object
        :rtype: objects.Response
        """
        resp = methods.unpin_message(self.__access_token, chat_id, self.__proxies)
        return objects.Response.de_json(resp)

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
        :return: On success, Response Object
        :rtype: objects.Response
        """
        resp = methods.leave_chat(self.__access_token, chat_id, self.__proxies)
        return objects.Response.de_json(resp)

    def get_chat_admins(self, chat_id):
        """
        Get all chat administrator, Bot must be administrator in requested chat
        :param int chat_id: chat identifier
        :return: On success, MemberInfo
        :rtype: objects.MemberInfo
        """
        resp = methods.get_chat_admins(self.__access_token, chat_id, self.__proxies)
        return objects.MemberInfo.de_json(resp)

    def get_chat_members(self, chat_id, user_ids=None, marker=None, count=20):
        """
        Get users participated in chat
        :param int chat_id: chat identifier
        :param list[int] or None user_ids: users identifier
        :param int or None marker: a Marker
        :param int count: Default 20, Count
        :return: On success, MemberInfo
        :rtype: objects.MemberInfo
        """
        resp = methods.get_members(self.__access_token, chat_id, user_ids, marker, count, self.__proxies)
        return objects.MemberInfo.de_json(resp)

    def add_members(self, chat_id, user_ids):
        """
        Adds members to chat
        :param int chat_id: chat identifier
        :param list[int] user_ids: users identifier
        :return: On success, Response Object
        :rtype: objects.Response
        """
        resp = methods.add_members(self.__access_token, chat_id, user_ids, self.__proxies)
        return objects.Response.de_json(resp)

    def remove_member(self, chat_id, user_ids, block=False):
        """
        Removes member for chat
        :param chat_id: chat identifier
        :param user_ids: users identifier
        :param block: Set to True if user should be blocked in chat
        :return: On success, Response Object
        :rtype: objects.Response
        """
        resp = methods.remove_member(self.__access_token, chat_id, user_ids, block, self.__proxies)
        return objects.Response.de_json(resp)

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
        :return: On success, Response Object
        :rtype: objects.Response
        """
        resp = methods.edit_message(self.__access_token, message_id, text, attachments, link, notify, formatter,
                                    self.__proxies)
        return objects.Response.de_json(resp)

    def delete_message(self, message_id):
        """
        Delete existing message
        :param str message_id: Message identifier
        :return: On success, Response Object
        :rtype: objects.Response
        """
        resp = methods.delete_message(self.__access_token, message_id, self.__proxies)
        return objects.Response.de_json(resp)

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
        :return: On success, Response Object
        :rtype: objects.Response
        """
        resp = methods.answer_on_callback(self.__access_token, callback_id, message, notification, self.__proxies)
        return objects.Response.de_json(resp)

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
        :return: On success, Response Object
        :rtype: objects.Response
        """
        resp = methods.construct_message(self.__access_token, session_id, messages, allow_user_input, hint, data,
                                         keyboard, placeholder, self.__proxies)
        return objects.Response.de_json(resp)

    def get_subscriptions(self):
        """
        In case your bot gets data via WebHook, the method returns list of all subscriptions
        :return: On Success, Array of Subscriptions object
        :rtype: list[objects.Subscription]
        """
        resp = methods.get_subscriptions(self.__access_token, self.__proxies)
        subscriptions = []
        for x in resp:
            subscriptions.append(objects.Subscription.de_json(x))
        return subscriptions

    def subscribe(self, url, update_types=None, version=None):
        """
        Subscribes bot to receive updates via WebHook
        :param str url: URL of HTTP(S)-endpoint of your bot. Must starts with http(s)://
        :param list[str] or None update_types: List of update types your bot want to receive
        :param str or None version: Version of API, Affects model representation
        :return: On success, Response Object
        :rtype: objects.Response
        """
        resp = methods.subscribe(self.__proxies, url, update_types, version, self.__proxies)
        return objects.Response.de_json(resp)

    def unsubscribe(self, url):
        """
        Unsubscribes bot from receiving updates via WebHook
        :param str url:
        :return: On success, Response Object
        :rtype: objects.Response
        """
        resp = methods.unsubscribe(self.__access_token, url, self.__proxies)
        return objects.Response.de_json(resp)

    def get_updates(self, limit=100, timeout=30, marker=None, types=None):
        """
        You can use this method for getting updates in case your bot is not subscribed to WebHook,
        The method is based on long polling
        :param int limit: Maximum number of updates to be retrieved
        :param int timeout: Timeout in seconds for long polling
        :param int or None marker: Pass None to get updates you didn't get yet
        :param list[str] or None types: Comma separated list of update types your bot want to receive
        :return: On Success, UpdateInfo object
        :rtype: objects.UpdateInfo
        """
        resp = methods.get_update(self.__access_token, limit, timeout, marker, types, self.__proxies)
        return objects.UpdateInfo.de_json(resp)

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
