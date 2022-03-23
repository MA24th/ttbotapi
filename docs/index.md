# ttbotapi
[TamTam Bot API](https://dev.tamtam.chat) library

[![GPLv2 license](https://img.shields.io/badge/LICENSE-GPLv2-red)](https://github.com/ma24th/ttbotapi/blob/master/LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-v0.3.0-yellow.svg)](https://pypi.org/project/ttbotapi/)
[![Python package](https://github.com/MA24th/ttbotapi/workflows/Python%20package/badge.svg)](https://github.com/MA24th/ttbotapi/actions/workflows/python-package.yml)
[![TamTam Channel](https://img.shields.io/badge/TamTam-Channel-blue.svg)](https://tt.me/ttbotapic)

## How to Use
The Bot class encapsulates all API calls in a single class. It provides functions such as 
`send_xyz` (`send_message`, `edit_message` etc.) and several ways to listen for incoming messages.

Create a file called `echo_bot.py`.
Then, open the file and create an instance of the Bot class.
```python
import ttbotapi
import logging

ttbotapi.logger.setLevel(logging.DEBUG)

# Note: Make sure to actually replace TOKEN with your own API token.
bot = ttbotapi.Bot(access_token='Bot Token')

# After that declaration, we need to register some so-called decorator handlers.
# Update handlers define filters which a message must pass. If a message passes the filter, 
# the decorated function is called and the incoming message is passed as an argument.

# Let's define a message handler which handles incoming `/start` and `/help` bot_command in dialog chat type.
@bot.update_handler(chat_type='dialog', bot_command=['/start', '/help'])
def send_welcome(update):
    # A function which is decorated by an update handler can have an arbitrary name, 
    # however, it must have only one parameter (the update)
    bot.send_message(text="Howdy, how are you doing?", user_id=update.message.sender.user_id, chat_id=None,
                     link={'type': 'reply', 'mid': update.message.body.mid})

# Let's add another handler
@bot.update_handler(chat_type='dialog', regexp='hi')
def send_hi(update):
    bot.send_message(text=f'Hi 👋, {update.message.sender.name}', user_id=update.message.sender.user_id, chat_id=None)


# This one echoes all incoming text messages back to the sender. It uses a lambda function to test a message. 
# If the lambda returns True, the message is handled by the decorated function. 
# Since we want all messages to be handled by this function, we simply always return True.
@bot.update_handler(func=lambda update: update.message.body.text)
def echo(update):
    bot.send_message(text=update.message.body.text, user_id=update.message.sender.user_id, chat_id=None)


# Using long polling now our bot never stop working
bot.polling()

# Alright, that's it! Our source file now looks fine
```
To start the bot, simply open up a terminal and enter `python echo_bot.py` to run the bot! 
Test it by sending commands ('/start' and '/help') and arbitrary text messages.

### Explanation

A `handler` is a function that is decorated with the `update_handler` decorator of a Bot instance, handlers consist of
one or multiple filters, Each filter match returns True for a certain message in order for an update handler to become
eligible.

Here are some examples of using the filters and handlers:

| update_type                    | filters                                      | return types | function argument |
|--------------------------------|----------------------------------------------|--------------|-------------------|
| `message_callback`             | `chat_type`, `bot_command`, `regexp`, `func` | `Update`     | `update`          |
| `message_created`              | `chat_type`, `bot_command`, `regexp`, `func` | `Update`     | `update`          |
| `message_removed`              | `chat_type`, `bot_command`, `regexp`, `func` | `Update`     | `update`          |
| `message_edited`               | `chat_type`, `bot_command`, `regexp`, `func` | `Update`     | `update`          |
| `bot_added`                    | `regexp`, `func`                             | `Update`     | `update`          |
| `bot_removed`                  | `regexp`, `func`                             | `Update`     | `update`          |
| `user_added`                   | `regexp`, `func`                             | `Update`     | `update`          |
| `user_removed`                 | `regexp`, `func`                             | `Update`     | `update`          |
| `bot_started`                  | `regexp`, `func`                             | `Update`     | `update`          |
| `chat_title_change`            | `regexp`, `func`                             | `Update`     | `update`          |
| `message_construction_request` | `regexp`, `func`                             | `Update`     | `update`          |
| `message_constructed`          | `regexp`, `func`                             | `Update`     | `update`          |
| `message_chat_created`         | `regexp`, `func`                             | `Update`     | `update`          |

A `message_created` handler is declared in the following way:

```python
import ttbotapi

bot = ttbotapi.Bot(access_token="TOKEN")


@bot.update_handler(update_type='message_created')  # filters
def function_name(update):
    bot.send_message(chat_id=update.recipient.chat_id, user_id=None, text="This is a message handler")
```

`function_name` is not bound to any restrictions. Any function name is permitted with update handlers. The function must
accept at most one argument, which will be the message that the function must handle.

`filters` is a list of keyword arguments. A filter is declared in the following manner: `name=argument`. One handler may
have multiple filters.

Bot supports the following filters:

|    name     | argument(s)                                              | Condition                                                 |
|:-----------:|----------------------------------------------------------|-----------------------------------------------------------|
| update_type | list of strings or string, default `message_created`     | `True` if `update_type='message_created'`.                |
|  chat_type  | list of strings or string, (`dialog`, `chat`, `channel`) | `True` if `update.recipient.chat_type` in `chat_type`     |
| bot_command | list of strings or string, (`/start`)                    | `True` if `update.message.body.text` in `bot_command`     |
|    regex    | a regular expression as a string                         | `True` if `re.search(regexp_arg)` returns `True`          |
|    func     | a function, (lambda or function reference)               | `True` if the lambda or function reference returns `True` |



`Logging` You can use the ttbotapi module logger to log debug info about Bot.

It is possible to add custom logging Handlers to the logger,
Refer to the [Python logging](https://docs.python.org/3/library/logging.html) for more info.

```python
import logging
from ttbotapi import logger

logger.setLevel(logging.DEBUG) # Outputs debug messages to console.
```

## How to Contribute

- You must follow [Contributing](https://github.com/MA24th/MA24th/blob/main/OpenSource/Software/CONTRIBUTING.md)
  Guidelines.
- We are committed to providing a friendly community, for more experience
  read [Code Of Conduct](https://github.com/MA24th/MA24th/blob/main/OpenSource/Software/CODE_OF_CONDUCT.md).


## Attribution

These Documents are adapted
for [MA24th Open Source Software](https://github.com/MA24th/MA24th/blob/main/OpenSource/Software/),

For more information [Contact](mailto:ma24th@yahoo.com) with any additional questions or comments.