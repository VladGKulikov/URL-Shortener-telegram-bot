from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from unshortenit import UnshortenIt
import pyshorteners
import re
from pony.orm import *
import random

shortener = pyshorteners.Shortener(api_key='...') # !!!! Need your bitly api_key !!!!

db = Database()
db = Database("sqlite", "estore.sqlite", create_db=True)


class Person(db.Entity):
    short_link = Required(str)


# sql_debug(True)
db.generate_mapping(create_tables=True)


def start(update, context):
    first_name = update.message.chat.first_name
    update.message.reply_text('What\'s up ' + str(first_name) + ' !!! How are you?!' +
                              '\n\n👣 How are your kids, how is your family? Good??!!!' +
                              '\n👣 I\'m👻 happy for you!!!!👌 👍' +
                              '\n👣\n👣 Welcome to Short Link Bot for SD & Python course in MSAI.' +
                              '\n👣 I can short long urls , and also unshort various short urls.' +
                              '\n👣\n👣 And forgive me! I will save your links that you cut in my DB !!!!' +
                              '\n👣 I did not want! They made me!!!🙈 🙉 🙊 I\'m crying😭😭😭 )) ' +
                              '\n👣\n👣 Type /help to know how to use this 👽very strange👽 bot.')


def help(update, context):
    update.message.reply_text(
        'Just send the url that you want to short or unshort.' +
        '\n\n❗❗❗👇 Url must start with 👇❗❗❗' +
        '\n\n🆗 http:// 🆗' +
        '\n🆗 https:// 🆗' +
        '\n\n❌And it should not have spaces in it.❌' +
        '\n\nI have next command now :' +
        '\n/start - Well, it\'s kind of a start...' +
        '\n/help - ??? This is the help!!!! H.e.l.p.!!!!! 🍒 🍒 🍒 ))) ' +
        '\n\nType /history to know all the links what I short.' +
        '\n\nAnd ... /factorial - if you love factorials and want to see random factorial ≤ 10^6)))) !!!!!' +
        '\nIt\'s will be not so slow, but.... this is fun!!!!' +
        '\nFor my code: 10^6 - 1 min... ' +
        '\nBut it\'s sad.....😭😭😭😭😭' +
        '\nTelegram told me ...AAAAA!!!!! -' +
        '\n👿👿👿👿👿 - the message is too long for 10^6 👿👿👿👿👿' +
        '\nBut ... ok... only ≤ 10^3')


def convert(update, context):
    global link
    link = update.message.text
    pattern1 = "https://*"
    pattern2 = "http://*"
    if (re.search(pattern1, link)) or (re.search(pattern2, link)):
        keyboard = [[InlineKeyboardButton("Short", callback_data='short'),
                     InlineKeyboardButton("Unshort", callback_data='unshort')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Select from the below options whether you want to short or unshort your url',
                                  reply_markup=reply_markup)
    else:
        update.message.reply_text(
            '😡️😈️😡️ Url ... must ... start .... with ....😡️😈️😡️' +
            '\nhttp:// or https://' +
            '\nand it should not have spaces in it.',
            parse_mode=telegram.ParseMode.HTML)


@db_session
def button(update, context):
    query = update.callback_query
    query.answer()
    a = query.data
    if a == "unshort":
        unshortener = UnshortenIt()
        uri = unshortener.unshorten(link)
        query.edit_message_text(text="Unshorted url 👇🏼 : \n" + str(uri))
    if a == "short":
        try:
            response = shortener.bitly.short(link)
        except pyshorteners.exceptions.ShorteningErrorException:
            query.edit_message_text(text='❓👀❓👀❓ Ha! This is 👆 already short link')
        else:
            query.edit_message_text("Shorted url 👇🏼:\n" + str(response))
            Person(short_link=str(response))
            commit()


@db_session
def history(update, context):
    persons = select(p for p in Person)[:]
    res = ''
    for i in persons:
        res = '\n' + i.short_link + res
    update.message.reply_text(f'This are all short links that I made: {res}')


def prod_tree(l, h):
    if l + 1 < h:
        mid = (h + l) // 2
        return prod_tree(l, mid) * prod_tree(mid + 1, h)
    if l == h:
        return l
    return l * h


def tree_factorial(n):
    return 1 if n < 2 else prod_tree(1, n)


def factorial(update, context):
    k = int(random.uniform(0, 1000))
    f = tree_factorial(k)
    update.message.reply_text(f'Factorial {k} :\n{f}' +
                              '\n🔥🔥🔥🔥🔥Haaaaa!!!!! Very cool!!!!!🔥🔥🔥🔥' + '\nIsn\'t it?')


def main():
    token = "..." # !!!! Need your telegram token !!!! 
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('history', history))
    dp.add_handler(CommandHandler('factorial', factorial))
    dp.add_handler(MessageHandler(Filters.text, convert))
    dp.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
