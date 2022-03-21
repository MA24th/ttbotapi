# -*- coding: utf-8 -*-

"""
ttbotapi.methods
~~~~~~~~~~~~~~~~
This submodule provides a TamTam Available methods,
All methods in the Bot API are case-insensitive,
On successful call, a JSON-object containing the result will be returned.
:copyright: (c) 2022 by Mustafa Asaad.
:license: GPLv2, see LICENSE for more details.
"""
from .utils import make_request


# bots
def get_bot_info(access_token, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'GET'
    api_method = r'me'
    api_url = f'{based_url}/{api_method}?access_token={access_token}'
    files = None
    params = None
    return make_request(http_method, api_method, api_url, files, params, proxies)


def edit_bot_info(access_token, name, username, description, commands, photo, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'PATCH'
    api_method = r'me'
    api_url = f'{based_url}/{api_method}?access_token={access_token}'
    files = None
    body = {}
    if name:
        body['name'] = name
    if username:
        body['username'] = username
    if description:
        body['description'] = description
    if commands:
        body['commands'] = commands
    if photo:
        body['photo'] = photo
    return make_request(http_method, api_method, api_url, files, body, proxies)


#######################################################################################################################
# chats
def get_all_chats(access_token, count, marker, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'GET'
    api_method = r'chats'
    api_url = f'{based_url}/{api_method}?access_token={access_token}'
    files = None
    params = {}
    if count:
        params['count'] = count
    if marker:
        params['marker'] = marker
    return make_request(http_method, api_method, api_url, files, params, proxies)


def get_chat_by_link(access_token, chat_link, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'GET'
    api_method = r'chats'
    api_url = f'{based_url}/{api_method}/{chat_link}?access_token={access_token}'
    return make_request(http_method, api_method, api_url, proxies)


def get_chat(access_token, chat_id, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'GET'
    api_method = r'chats'
    api_url = f'{based_url}/{api_method}/{chat_id}?access_token={access_token}'
    return make_request(http_method, api_method, api_url, proxies)


def edit_chat_info(access_token, chat_id, icon, title, pin, notify, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'PATCH'
    api_method = r'chats'
    api_url = f'{based_url}/{api_method}/{chat_id}?access_token={access_token}'
    body = {}
    if icon:
        body['icon'] = icon
    if title:
        body['title'] = title
    if pin:
        body['pin'] = pin
    if notify:
        body['notify'] = notify
    return make_request(http_method, api_method, api_url, body, proxies)


def send_action(access_token, chat_id, action, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'POST'
    api_method = r'chats'
    api_url = f'{based_url}/{api_method}/{chat_id}?access_token={access_token}'
    body = {'action': action}
    return make_request(http_method, api_method, api_url, body, proxies)


def get_pinned_message(access_token, chat_id, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'GET'
    api_method = r'chats'
    api_url = f'{based_url}/{api_method}/{chat_id}/pin?access_token={access_token}'
    return make_request(http_method, api_method, api_url, proxies)


def pin_message(access_token, chat_id, message_id, notify, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'PUT'
    api_method = r'chats'
    api_url = f'{based_url}/{api_method}/{chat_id}/pin?access_token={access_token}'
    body = {'message_id': message_id, 'notify': notify}
    return make_request(http_method, api_method, api_url, body, proxies)


def unpin_message(access_token, chat_id, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'DELETE'
    api_method = r'chats'
    api_url = f'{based_url}/{api_method}/{chat_id}/pin?access_token={access_token}'
    return make_request(http_method, api_method, api_url, proxies)


def get_chat_membership(access_token, chat_id, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'GET'
    api_method = r'chats'
    api_url = f'{based_url}/{api_method}/{chat_id}/members/me?access_token={access_token}'
    return make_request(http_method, api_method, api_url, proxies)


def leave_chat(access_token, chat_id, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'DELETE'
    api_method = r'chats'
    api_url = f'{based_url}/{api_method}/{chat_id}/members/me?access_token={access_token}'
    return make_request(http_method, api_method, api_url, proxies)


def get_chat_admins(access_token, chat_id, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'GET'
    api_method = r'chats'
    api_url = f'{based_url}/{api_method}/{chat_id}/members/admins?access_token={access_token}'
    return make_request(http_method, api_method, api_url, proxies)


def get_members(access_token, chat_id, user_ids, marker, count, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'GET'
    api_method = r'chats'
    api_url = f'{based_url}/{api_method}/{chat_id}/members?access_token={access_token}'
    params = {}
    if user_ids:
        params['user_ids'] = user_ids
    if marker:
        params['marker'] = marker
    if count:
        params['count'] = count
    return make_request(http_method, api_method, api_url, params, proxies)


def add_members(access_token, chat_id, user_ids, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'POST'
    api_method = r'chats'
    api_url = f'{based_url}/{api_method}/{chat_id}/members?access_token={access_token}'
    body = {}
    if user_ids:
        body['user_ids'] = user_ids
    return make_request(http_method, api_method, api_url, body, proxies)


def remove_member(access_token, chat_id, user_id, block, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'DELETE'
    api_method = r'chats'
    api_url = f'{based_url}/{api_method}/{chat_id}/members?access_token={access_token}'
    params = {}
    if user_id:
        params['user_id'] = user_id
    if block:
        params['block'] = block
    return make_request(http_method, api_method, api_url, params, proxies)


#######################################################################################################################
# messages
def get_messages(access_token, chat_id, message_ids, ffrom, to, count, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'GET'
    api_method = r'messages'
    api_url = f'{based_url}/{api_method}?access_token={access_token}'
    params = {}
    if chat_id:
        params['chat_id'] = chat_id
    if message_ids:
        params['message_ids'] = message_ids
    if ffrom:
        params['from'] = ffrom
    if to:
        params['to'] = to
    if count:
        params['count'] = count
    return make_request(http_method, api_method, api_url, params, proxies)


def send_message(access_token, user_id, chat_id, disable_link_preview, text, attachments, link, notify, formatter,
                 proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'POST'
    api_method = r'messages'
    api_url = f'{based_url}/{api_method}?access_token={access_token}'
    params = {}
    if user_id:
        params['user_id'] = user_id
    if chat_id:
        params['chat_id'] = chat_id
    if disable_link_preview:
        params['disable_link_preview'] = disable_link_preview
    body = {}
    if text:
        body['text'] = text
    if attachments:
        body['attachments'] = attachments
    if link:
        body['link'] = link
    if notify:
        body['notify'] = notify
    if formatter:
        body['format'] = formatter
    return make_request(http_method, api_method, api_url, params, body, proxies)


def edit_message(access_token, message_id, text, attachments, link, notify, formatter, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'PUT'
    api_method = r'messages'
    api_url = f'{based_url}/{api_method}?access_token={access_token}'
    params = {}
    if message_id:
        params['message_id'] = message_id
    body = {}
    if text:
        body['text'] = text
    if attachments:
        body['attachments'] = attachments
    if link:
        body['link'] = link
    if notify:
        body['notify'] = notify
    if formatter:
        body['format'] = formatter
    return make_request(http_method, api_method, api_url, params, body, proxies)


def delete_message(access_token, message_id, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'DELETE'
    api_method = r'messages'
    api_url = f'{based_url}/{api_method}?access_token={access_token}'
    params = {}
    if message_id:
        params['message_id'] = message_id
    return make_request(http_method, api_method, api_url, params, proxies)


def get_message(access_token, message_id, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'GET'
    api_method = r'messages'
    api_url = f'{based_url}/{api_method}/{message_id}?access_token={access_token}'
    return make_request(http_method, api_method, api_url, proxies)


def answer_on_callback(access_token, callback_id, message, notification, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'POST'
    api_method = r'answer'
    api_url = f'{based_url}/{api_method}/{callback_id}?access_token={access_token}'
    body = {}
    if message:
        body['message'] = message
    if notification:
        body['notification'] = notification
    return make_request(http_method, api_method, api_url, body, proxies)


def construct_message(access_token, session_id, messages, allow_user_input, hint, data, keyboard, placeholder, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'POST'
    api_method = r'answer'
    api_url = f'{based_url}/{api_method}/constructor?access_token={access_token}'
    params = {'session_id': session_id}
    body = {}
    if messages:
        body['messages'] = messages
    if allow_user_input:
        body['allow_user_input'] = allow_user_input
    if hint:
        body['hint'] = hint
    if data:
        body['data'] = data
    if keyboard:
        body['keyboard'] = keyboard
    if placeholder:
        body['placeholder'] = placeholder
    return make_request(http_method, api_method, api_url, params, body, proxies)


#######################################################################################################################
# subscriptions
def get_subscriptions(access_token, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'GET'
    api_method = r'subscription'
    api_url = f'{based_url}/{api_method}?access_token={access_token}'
    return make_request(http_method, api_method, api_url, proxies)


def subscribe(access_token, url, update_types, version, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'POST'
    api_method = r'subscription'
    api_url = f'{based_url}/{api_method}?access_token={access_token}'
    body = {}
    if url:
        body['url'] = url
    if update_types:
        body['update_types'] = update_types
    if version:
        body['version'] = version
    return make_request(http_method, api_method, api_url, body, proxies)


def unsubscribe(access_token, url, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'DELETE'
    api_method = r'subscription'
    api_url = f'{based_url}/{api_method}?access_token={access_token}'
    params = {}
    if url:
        params['url'] = url
    return make_request(http_method, api_method, api_url, params, proxies)


def get_update(access_token, limit, timeout, marker, types, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'GET'
    api_method = r'updates'
    api_url = f'{based_url}/{api_method}?access_token={access_token}'
    params = {}
    if limit:
        params['limit'] = limit
    if timeout:
        params['timeout'] = timeout
    if marker:
        params['marker'] = marker
    if types:
        params['types'] = types
    return make_request(http_method, api_method, api_url, params, proxies)


######################################################################################################################
# upload
def get_upload_url(access_token, data, ttype, proxies):
    based_url = 'https://botapi.tamtam.chat'
    http_method = 'POST'
    api_method = r'uploads'
    api_url = f'{based_url}/{api_method}?access_token={access_token}'
    params = {}
    if ttype:
        params['type'] = ttype
    return make_request(http_method, api_method, api_url, data, params, proxies)
