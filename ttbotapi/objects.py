# -*- coding: utf-8 -*-

"""
ttbotapi.objects
~~~~~~~~~~~~~~~~
This submodule provides a TamTam Available objects,
All objects used in the Bot API responses are represented as JSON-objects.
:copyright: (c) 2022 by Mustafa Asaad.
:license: GPLv2, see LICENSE for more details.
"""
from .utils import JsonDeserializable, JsonSerializable


class User(JsonDeserializable):
    def __init__(self, user_id, name, username, is_bot, last_activity_time, description, avatar_url, full_avatar_url,
                 commands):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.is_bot = is_bot
        self.last_activity_time = last_activity_time
        self.description = description
        self.avatar_url = avatar_url
        self.full_avatar_url = full_avatar_url
        self.commands = commands

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        user_id = obj['user_id']
        name = obj['name']
        username = obj['username']
        is_bot = obj['is_bot']
        last_activity_time = obj['last_activity_time']
        description = None
        if 'description' in obj:
            description = obj['description']
        avatar_url = None
        if 'avatar_url' in obj:
            avatar_url = obj['avatar_url']
        full_avatar_url = None
        if 'full_avatar_url' in obj:
            full_avatar_url = obj['full_avatar_url']
        commands = None
        if 'commands' in obj:
            commands = User.parse_commands(obj['commands'])
        return cls(user_id, name, username, is_bot, last_activity_time, description, avatar_url, full_avatar_url,
                   commands)

    @staticmethod
    def parse_commands(obj):
        commands = []
        for x in obj:
            commands.append(BotCommand.de_json(x))
        return commands


class Chat(JsonDeserializable):
    def __init__(self, chat_id, ttype, status, title, icon, last_event_time, participants_count, owner_id, participants,
                 is_public, link, description, dialog_with_user, messages_count, chat_message_id, pinned_message):
        self.chat_id = chat_id
        self.ttype = ttype
        self.status = status
        self.title = title
        self.icon = icon
        self.last_event_time = last_event_time
        self.participants_count = participants_count
        self.owner_id = owner_id
        self.participants = participants
        self.is_public = is_public
        self.link = link
        self.description = description
        self.dialog_with_user = dialog_with_user
        self.messages_count = messages_count
        self.chat_message_id = chat_message_id
        self.pinned_message = pinned_message

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        chat_id = obj['chat_id']
        ttype = obj['type']
        status = obj['status']
        title = obj['title']
        icon = obj['icon']
        last_event_time = obj['last_event_time']
        participants_count = obj['participants_count']
        owner_id = obj['owner_id']
        participants = obj['participants']
        is_public = obj['is_public']
        link = obj['link']
        description = obj['description']
        dialog_with_user = User.de_json(obj['dialog_with_user'])
        messages_count = obj['messages_count']
        chat_message_id = obj['chat_message_id']
        pinned_message = Message.de_json(obj['pinned_message'])
        return cls(chat_id, ttype, status, title, icon, last_event_time, participants_count, owner_id, participants,
                   is_public, link, description, dialog_with_user, messages_count, chat_message_id, pinned_message)


class Message(JsonDeserializable):
    def __init__(self, sender, recipient, timestamp, link, body, stat, url, constructor):
        self.sender = sender
        self.recipient = recipient
        self.timestamp = timestamp
        self.link = link
        self.body = body
        self.stat = stat
        self.url = url
        self.constructor = constructor

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        sender = User.de_json(obj['sender'])
        recipient = obj['recipient']
        timestamp = obj['timestamp']
        link = obj['link']
        body = obj['body']
        stat = obj['stat']
        url = obj['url']
        constructor = obj['constructor']
        return cls(sender, recipient, timestamp, link, body, stat, url, constructor)


class NewMessage(JsonDeserializable):
    def __init__(self, text, attachments, link, notify, formatted):
        self.text = text
        self.attachments = attachments
        self.link = link
        self.notify = notify
        self.formatted = formatted

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        text = obj['text']
        attachment = obj['attachment']
        link = obj['link']
        notify = obj['notify']
        formatted = obj['format']
        return cls(text, attachment, link, notify, formatted)


class Update(JsonDeserializable):
    def __init__(self, update_type, timestamp, callback, message, user_locale, message_id, chat_id, user_id, session_id,
                 inviter_id, admin_id, user, is_channel, payload, title, data, iinput, start_payload):
        self.update_type = update_type
        self.timestamp = timestamp
        self.callback = callback
        self.message = message
        self.user_locale = user_locale
        self.message_id = message_id
        self.chat_id = chat_id
        self.user_id = user_id
        self.session_id = session_id
        self.inviter_id = inviter_id
        self.admin_id = admin_id
        self.user = user
        self.is_channel = is_channel
        self.payload = payload
        self.title = title
        self.data = data
        self.iinput = iinput
        self.start_payload = start_payload

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        update_type = obj['update_type']
        timestamp = obj['timestamp']
        callback = None
        if 'callback' in obj:
            callback = obj['callback']
        message = None
        if 'message' in obj:
            message = obj['message']
        user_locale = None
        if 'user_locale' in obj:
            user_locale = obj['user_locale']
        message_id = None
        if 'message_id' in obj:
            message_id = obj['message_id']
        chat_id = None
        if 'chat_id' in obj:
            chat_id = obj['chat_id']
        user_id = None
        if 'user_id' in obj:
            user_id = obj['user_id']
        session_id = None
        if 'session_id' in obj:
            session_id = obj['session_id']
        inviter_id = None
        if 'inviter_id' in obj:
            inviter_id = obj['inviter_id']
        admin_id = None
        if 'admin_id' in obj:
            admin_id = obj['admin_id']
        user = None
        if 'user' in obj:
            user = User.de_json(obj['user'])
        is_channel = None
        if 'is_channel' in obj:
            is_channel = obj['is_channel']
        payload = None
        if 'payload' in obj:
            payload = obj['payload']
        title = None
        if 'title' in obj:
            title = obj['title']
        data = None
        if 'data' in obj:
            data = obj['data']
        iinput = None
        if 'input' in obj:
            iinput = obj['input']
        start_payload = None
        if 'start_payload' in obj:
            start_payload = obj['start_payload']
        return cls(update_type, timestamp, callback, message, user_locale, message_id, chat_id, user_id, session_id,
                   inviter_id, admin_id, user, is_channel, payload, title, data, iinput, start_payload)


class BotCommand(JsonDeserializable, JsonSerializable):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        name = obj['name']
        description = obj['description']
        return cls(name, description)

    def to_dict(self):
        obj = {"name": self.name, "description": self.description}
        return obj
