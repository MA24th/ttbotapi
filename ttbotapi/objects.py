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


class Response(JsonDeserializable):
    def __init__(self, success, message):
        self.success = success
        self.message = message

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        success = obj['success']
        message = obj['message']
        return cls(success, message)


class MemberInfo(JsonDeserializable):
    def __init__(self, members, marker):
        self.members = members
        self.marker = marker

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        members = obj['members']
        marker = obj['marker']
        return cls(members, marker)

    @staticmethod
    def parse_members(obj):
        members = []
        for x in obj:
            members.append(User.de_json(x))


class User(JsonDeserializable):
    def __init__(self, user_id, name, username, is_bot, last_activity_time, description, avatar_url, full_avatar_url,
                 commands, last_access_time, is_owner, is_admin, join_time, permissions):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.is_bot = is_bot
        self.last_activity_time = last_activity_time
        self.description = description
        self.avatar_url = avatar_url
        self.full_avatar_url = full_avatar_url
        self.commands = commands
        self.last_access_time = last_access_time
        self.is_owner = is_owner
        self.is_admin = is_admin
        self.join_time = join_time
        self.permissions = permissions

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        user_id = obj['user_id']
        name = obj['name']
        username = None
        if 'username' in obj:
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
        last_access_time = None
        if 'last_access_time' in obj:
            last_access_time = obj['last_access_time']
        is_owner = False
        if 'is_owner' in obj:
            is_owner = obj['is_owner']
        is_admin = False
        if 'is_admin' in obj:
            is_admin = obj['is_admin']
        join_time = False
        if 'join_time' in obj:
            join_time = obj['join_time']
        permissions = False
        if 'permissions' in obj:
            permissions = Permissions.de_json(obj['permissions'])
        return cls(user_id, name, username, is_bot, last_activity_time, description, avatar_url, full_avatar_url,
                   commands, last_access_time, is_owner, is_admin, join_time, permissions)

    @staticmethod
    def parse_commands(obj):
        commands = []
        for x in obj:
            commands.append(BotCommand.de_json(x))
        return commands


class Permissions(JsonDeserializable):
    def __init__(self, read_all_messages, add_remove_members, add_admins, change_chat_info, pin_message, write):
        self.read_all_messages = read_all_messages
        self.add_remove_members = add_remove_members
        self.add_admins = add_admins
        self.change_chat_info = change_chat_info
        self.pin_message = pin_message
        self.write = write

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        read_all_messages = False
        if 'read_all_messages' in obj:
            read_all_messages = True
        add_remove_members = False
        if 'add_remove_members' in obj:
            add_remove_members = True
        add_admins = False
        if 'add_admins' in obj:
            add_admins = True
        change_chat_info = False
        if 'change_chat_info' in obj:
            change_chat_info = True
        pin_message = False
        if 'pin_message' in obj:
            pin_message = True
        write = False
        if 'write' in obj:
            write = True
        return cls(read_all_messages, add_remove_members, add_admins, change_chat_info, pin_message, write)


class Recipient(JsonDeserializable):
    def __init__(self, chat_id, chat_type, user_id):
        self.chat_id = chat_id
        self.chat_type = chat_type
        self.user_id = user_id

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        chat_id = obj['chat_id']
        chat_type = obj['chat_type']
        user_id = obj['user_id']
        return cls(chat_id, chat_type, user_id)


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
        title = None
        if 'title' in obj:
            title = obj['title']
        icon = None
        if 'icon' in obj:
            icon = obj['icon']
        last_event_time = obj['last_event_time']
        participants_count = obj['participants_count']
        owner_id = None
        if 'owner_id' in obj:
            owner_id = obj['owner_id']
        participants = None
        if 'participants' in obj:
            participants = obj['participants']
        is_public = None
        if 'is_public' in obj:
            is_public = obj['is_public']
        link = None
        if 'link' in obj:
            link = obj['link']
        description = None
        if 'description' in obj:
            description = obj['description']
        dialog_with_user = None
        if 'dialog_with_user' in obj:
            dialog_with_user = User.de_json(obj['dialog_with_user'])
        messages_count = None
        if 'messages_count' in obj:
            messages_count = obj['messages_count']
        chat_message_id = None
        if 'chat_message_id' in obj:
            chat_message_id = obj['chat_message_id']
        pinned_message = None
        if 'pinned_message' in obj:
            pinned_message = Message.de_json(obj['pinned_message'])
        return cls(chat_id, ttype, status, title, icon, last_event_time, participants_count, owner_id, participants,
                   is_public, link, description, dialog_with_user, messages_count, chat_message_id, pinned_message)


class ChatInfo(JsonDeserializable):
    def __init__(self, chats, marker):
        self.chats = chats
        self.marker = marker

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        chats = ChatInfo.parse_chats(obj['chat_id'])
        marker = obj['marker']
        return cls(chats, marker)

    @staticmethod
    def parse_chats(obj):
        chats = []
        for x in obj:
            chats.append(Chat.de_json(x))
        return chats


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
        sender = None
        if 'sender' in obj:
            sender = User.de_json(obj['sender'])
        recipient = None
        if 'recipient' in obj:
            recipient = Recipient.de_json(obj['recipient'])
        timestamp = None
        if 'timestamp' in obj:
            timestamp = obj['timestamp']
        link = None
        if 'link' in obj:
            link = obj['link']
        body = None
        if 'body' in obj:
            body = Body.de_json(obj['body'])
        stat = None
        if 'stat' in obj:
            stat = obj['stat']
        url = None
        if 'url' in obj:
            url = obj['url']
        constructor = None
        if 'constructor' in obj:
            constructor = obj['constructor']
        return cls(sender, recipient, timestamp, link, body, stat, url, constructor)


class NewMessage(JsonDeserializable):
    def __init__(self, text, attachments, link, notify, formatter):
        self.text = text
        self.attachments = attachments
        self.link = link
        self.notify = notify
        self.formatter = formatter

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        text = obj['text']
        attachment = NewMessage.parse_attachment(obj['attachment'])
        link = obj['link']
        notify = None
        if 'notify' in obj:
            notify = obj['notify']
        formatter = None
        if 'format' in obj:
            formatter = obj['format']
        return cls(text, attachment, link, notify, formatter)

    @staticmethod
    def parse_attachment(obj):
        attachments = []
        for x in obj:
            attachments.append(Attachment.de_json(x))
        return attachments


class Attachment(JsonDeserializable):
    def __init__(self, ttype, payload):
        self.ttype = ttype
        self.payload = payload

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        ttype = obj['type']
        payload = None
        if 'payload' in obj:
            payload = obj['payload']
        return cls(ttype, payload)


class Body(JsonDeserializable):
    def __init__(self, mid, seq, text, attachments, markup):
        self.mid = mid
        self.seq = seq
        self.text = text
        self.attachments = attachments
        self.markup = markup

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        mid = obj['mid']
        seq = obj['seq']
        text = obj['text']
        attachments = None
        if 'attachments' in obj:
            attachments = Body.parse_attachments(obj['attachments'])
        markup = None
        if 'markup' in obj:
            markup = Body.parse_markup(obj['markup'])
        return cls(mid, seq, text, attachments, markup)

    @staticmethod
    def parse_attachments(obj):
        attachments = []
        for x in obj:
            attachments.append(Attachment.de_json(x))
        return attachments

    @staticmethod
    def parse_markup(obj):
        markups = []
        for x in obj:
            markups.append(MarkupElement.de_json(x))
        return markups


class MarkupElement(JsonDeserializable):
    def __init__(self, ttype, ffrom, length, url, user_link, user_id):
        self.ttype = ttype
        self.ffrom = ffrom
        self.length = length
        self.url = url
        self.user_link = user_link
        self.user_id = user_id

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        ttype = obj['type']
        ffrom = obj['from']
        length = obj['length']
        url = None
        if 'url' in obj:
            url = obj['url']
        user_link = None
        if 'user_link' in obj:
            user_link = obj['user_link']
        user_id = None
        if 'user_id' in obj:
            user_id = obj['user_id']
        return cls(ttype, ffrom, length, url, user_link, user_id)


class Subscription(JsonDeserializable):
    def __init__(self, url, time, update_types, version):
        self.url = url
        self.time = time
        self.update_types = update_types
        self.version = version

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        url = None
        if 'url' in obj:
            url = obj['url']
        time = None
        if 'time' in obj:
            time = obj['time']
        update_types = None
        if 'update_types' in obj:
            update_types = obj['update_types']
        version = None
        if 'version' in obj:
            version = obj['version']
        return cls(url, time, update_types, version)


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
            message = Message.de_json(obj['message'])
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


class UpdateInfo(JsonDeserializable):
    def __init__(self, updates, marker):
        self.updates = updates
        self.marker = marker

    @classmethod
    def de_json(cls, obj_type):
        obj = cls.check_type(obj_type)
        updates = UpdateInfo.parse_updates(obj['updates'])
        marker = obj['marker']
        return cls(updates, marker)

    @staticmethod
    def parse_updates(obj):
        updates = []
        for x in obj:
            updates.append(Update.de_json(x))
        return updates


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
