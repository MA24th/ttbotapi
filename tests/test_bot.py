import ttbotapi
import logging

ttbotapi.logger.setLevel(logging.DEBUG)

bot = ttbotapi.Bot(access_token='gyFquBeqbECPlcVoOzSQtmBIDdzTWtSem0p9361Z7lI')

# bot.get_bot_info()
# bot.edit_bot_info(name='tgbotapi')
# bot.get_all_chats()
# bot.get_chat_by_link(chat_link='-82668540089870')
# bot.get_chat(chat_link='-82668540089870')
# bot.edit_chat_info(chat_id=-82668540089870, title='ttbotapi group')
# bot.send_action(chat_id=57816329950, action='typing')
x = bot.get_pinned_message(chat_id=-82668540089870)
print(x.body.markup)
# bot.pin_message(chat_id=-82668540089870, message_id="cLBp8_zWQv6qM6GqK5XxT5lnDsYhtRiz3YO4j2ugtrM")
# bot.unpin_message(chat_id=-82668540089870)
# bot.get_chat_membership(chat_id=57816329950)
# bot.leave_chat(chat_id=57816329950)
# bot.get_chat_admins(chat_id=57816329950)
# bot.get_chat_members(chat_id=57816329950)
# bot.add_members(chat_id=57816329950, user_ids=[595079508494])
# bot.remove_member(chat_id=57816329950, user_ids=[595079508494])
# bot.get_messages()
# bot.send_message(text='hi', chat_id=None, user_id=57816329950)
# bot.edit_message(message_id='2', text='hhhh')
# bot.delete_message(message_id='2')
# bot.get_message(message_id='2')
# bot.answer_on_callback(callback_id='2')
# bot.construct_message(session_id='2')
# bot.get_subscriptions()
# bot.subscribe(url='https://ma24th.github.io/ttbotapi')
# bot.unsubscribe(url='https://ma24th.github.io/ttbotapi')
# bot.get_updates()
# bot.get_upload_url(data='', ttype='photo')
