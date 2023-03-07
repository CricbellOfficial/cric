import os
import socket
from io import BytesIO
from queue import Queue
import requests
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Dispatcher
from movies_scraper import search_movies, get_movie


TOKEN = os.getenv("TOKEN")
URL = "https://cricketdreambot.vercel.app"
bot = Bot(TOKEN)
msgid = ""
chatid = ""
x = 0

def welcome(update, context) -> None:
    update.message.reply_text(f"Hello *{update.message.from_user.first_name}* \n Welcome To Our Cricket Fan Group.\n"
                              f"🔥 Search It 💯  Enjoy it  🍿")
    #update.message.reply_text("👇 Type Movie Or Series Name 👇")


def find_movie(update, context):
    search_results = update.message.reply_text("🔥 Searching.... Pls Wait..💯")
    query = update.message.text
    movies_list = search_movies(query)
    
    if movies_list:
        keyboards = []
        for movie in movies_list:
            keyboard = InlineKeyboardButton(movie["title"], callback_data=movie["id"])
            keyboards.append([keyboard])
        reply_markup = InlineKeyboardMarkup(keyboards)
        search_results.edit_text('Here I found - Pls Select One..!', reply_markup=reply_markup)
    else:
        search_results.edit_text('Sorry Not Found ! Check Your Spelling or')
       
            
          

    
    
def movie_result(update, context) -> None:
    query = update.callback_query
    msgid = query.message.message_id
    chatid = query.message.chat.id
    s = get_movie(query.data)
    response = requests.get("https://graph.org/file/98a7d42968319f27bc804.jpg")
    img = BytesIO(response.content)
    
    
    keyboards = []
    pick = s['pick']
    pp = s['t1']
    
    text = f"team1:{pp}"
    m = query.message.reply_photo(photo=img, caption=f"🎥 s['title']")
    global msgid1
    msgid1 = m["message_id"]
    request = InlineKeyboardButton(pick, url="https://t.me/fzfilmyzilla")
    keyboards.append([request])
    
    reply_markup = InlineKeyboardMarkup(keyboards)
    query.message.reply_text('#cricbell_expert', reply_markup=reply_markup)
    m = query.message.reply_text(pick)
    idd = m.message_id
    m.edit_text("◼️◻️◻️◻️◻️◻️◻️◻️◻️◻️")
    m.edit_text("◼️◼️◼️◻️◻️◻️◻️◻️◻️◻️")
    m.edit_text("◼️◼️◼️◼️◼️◻️◻️◻️◻️◻️")
    m.edit_text("◼️◼️◼️◼️◼️◼️◼️◻️◻️◻️")
    m.edit_text("◼️◼️◼️◼️◼️◼️◼️◼️◻️◻️")
    m.edit_text("◼️◼️◼️◼️◼️◼️◼️◼️◼️◼️")

   


def setup():
    update_queue = Queue()
    dispatcher = Dispatcher(bot, update_queue, use_context=True)
    dispatcher.add_handler(CommandHandler('start', welcome))
    dispatcher.add_handler(MessageHandler(Filters.text, find_movie))
    dispatcher.add_handler(CallbackQueryHandler(movie_result))
    return dispatcher

  
    

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/{}'.format(TOKEN), methods=['GET', 'POST'])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    setup().process_update(update)
    return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}/{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"
