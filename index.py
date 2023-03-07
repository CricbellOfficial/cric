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
    update.message.reply_text(f"Hello *{update.message.from_user.first_name}* \n 🏏 Welcome To Our Cricket Fan Group 🏏\n"
                              f"🔥 Predict it 💯  Win it  🍿")
    #update.message.reply_text("👇 Type Movie Or Series Name 👇")


def find_movie(update, context):
    search_results = update.message.reply_text("🔥 Todays Tips.... Pls Wait..💯")
    query = update.message.text
    movies_list = search_movies(query)
    
    if movies_list:
        keyboards = []
        for movie in movies_list:
            keyboard = InlineKeyboardButton(movie["title"], callback_data=movie["id"])
            keyboards.append([keyboard])
        reply_markup = InlineKeyboardMarkup(keyboards)
        search_results.edit_text('👇 Today Tips 👇!', reply_markup=reply_markup)
    else:
        #search_results.edit_text('Sorry Not Found ! Check Your Spelling or')
        ok = 'ok'
            
          

    
    
def movie_result(update, context) -> None:
    query = update.callback_query
    msgid = query.message.message_id
    chatid = query.message.chat.id
    s = get_movie(query.data)
    response = requests.get("https://graph.org/file/98a7d42968319f27bc804.jpg")
    img = BytesIO(response.content)
    
    
    keyboards = []
    pick = s['pick']
    t1 = s['t1']
    t2 = s['t2']
    #int(float(a))
    t1c = s['t1p']
    t2c = s['t2p']
    t1p = t1c.replace('%', '')
    t2p = t2c.replace('%', '')
    request = InlineKeyboardButton(pick, url="https://t.me/cricbellofficiall")
    keyboards.append([request])
    reply_markup = InlineKeyboardMarkup(keyboards)
    #query.message.reply_text('#cricbell_expert', reply_markup=reply_markup)
        
    k = query.message.reply_photo(photo=img, caption=f"🏆 {s['title']}\n⚠️Note: this Team Choice Before Toss\n For RUnning Updates Join Official Channel\n\n#CricbellExpert Today Team Choice\n👇 👇 👇 👇", reply_markup=reply_markup)
    global msgid1
    msgid1 = k["message_id"]
    text = f"{t1}⛹️‍♂️ Winning chances ⛹️‍♂️{t2}"

    m = query.message.reply_text(text)
    idd = m.message_id
    if 0 < int(float(t1p)) < 20:
        m.edit_text(f"{text}\n{t1c}◼️◻️◻️◻️◻️◻️{t2c}")
    elif 21 < int(float(t1p)) < 40:
        m.edit_text(f"{text}\n{t1c}◼️◼️◻️◻️◻️◻️{t2c}")
    elif 41 < int(float(t1p)) < 60:
        m.edit_text(f"{text}\n{t1c}◼️◼️◼️◻️◻️◻️{t2c}")
    elif 61 < int(float(t1p)) < 80:
        m.edit_text(f"{text}\n{t1c}◼️◼️◼️◼️◻️◻️{t2c}")
    elif 81 < int(float(t1p)) < 100:
        m.edit_text(f"{text}\n{t1c}◼️◼️◼️◼️◼️◻️{t2c}")
    else:
        ok = 'ok'
        m.edit_text("Running Update join our Official Channel")
   

   


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
