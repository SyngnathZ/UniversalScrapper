#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

import logging
import requests
from datetime import date
from configparser import ConfigParser

import telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = "5273937473:AAFUdluOex-tmpuPrbbNYlvODfmaDN809kY"
Group_id = '-1001594529120'

LoginUrl = 'https://synemby.filmind.club:8096/emby/Users/authenticatebyname?X-Emby-Client=Emby%20Web&X-Emby-Device-Name' \
           '=Chrome&X-Emby-Device-Id=f12333f8-a49c-4c73-9ea1-95756b0552e0&X-Emby-Client-Version=4.6.7.0 '
GetMoivesRank = 'https://synemby.filmind.club:8096/emby/user_usage_stats/MoviesReport'
GetTVsRank = 'https://synemby.filmind.club:8096/emby/user_usage_stats/TvShowsReport'

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def rank_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /rank is issued."""
    config = ConfigParser()
    config.read('config.ini')
    formdata = {'Username': config['Admin']['USER'], 'Pw': config['Admin']['PASSWORD']}
    session = requests.session()
    res = session.post(LoginUrl, data=formdata).json()
    today = date.today()
    params = {'days': '30', 'end_date': today, 'stampc': '1645197621843', 'X-Emby-Client': 'Emby Web',
              'X-Emby-Device-Name': 'X-Emby-Device-Name', 'X-Emby-Device-Id': 'f12333f8-a49c-4c73-9ea1-95756b0552e0',
              'X-Emby-Client-Version': '4.6.7.0', 'X-Emby-Token': res['AccessToken']}
    moviesRes = session.get(GetMoivesRank, params=params, timeout=15).json()
    tvsRes = session.get(GetTVsRank, params=params, timeout=15).json()
    moviesRes.sort(key=takecount, reverse=True)
    tvsRes.sort(key=takecount, reverse=True)

    RankRes = '今天看什么电影\n'
    for i in range(1, 11):
        RankRes = RankRes + str(i) + '. ' + moviesRes[i - 1]['label'] + ' - ' + str(moviesRes[i - 1]['count']) + '\n'

    RankRes += '\n今天看什么电视剧\n'
    for i in range(1, 11):
        RankRes = RankRes + str(i) + '. ' + tvsRes[i - 1]['label'] + ' - ' + str(tvsRes[i - 1]['count']) + '\n'

    RankRes += '\n上述统计数据截止到 ' + str(today)

    sendmsg(RankRes, Group_id, BOT_TOKEN)
    # update.message.reply_text(RankRes)


def takecount(elem):
    return elem['count']


def sendmsg(msg, chat_id, token=BOT_TOKEN):
    """
    Send a message to a telegram user or group specified on chatId
    chat_id must be a number!
    """
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)


#
# def echo(update: Update, context: CallbackContext) -> None:
#     """Echo the user message."""
#     update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("rank", rank_command))

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
