from flask import Flask, request
import requests
import os
import telebot

os.environ["PARSE_API_ROOT"] = "https://parseapi.back4app.com/"

app = Flask(__name__)

# Everything else same as usual

from parse_rest.datatypes import Function, Object, GeoPoint
from parse_rest.connection import register
from parse_rest.query import QueryResourceDoesNotExist
from parse_rest.connection import ParseBatcher
from parse_rest.core import ResourceRequestBadRequest, ParseError


APPLICATION_ID = 'Ts1A7Zvn3GBJGN62VyvYJEUiKEJwyIBSumxwiPRk'
REST_API_KEY = 'mjbuzgxCofRDnSCUU7yovyKyKdkfSZr9KvJYqpgi'
MASTER_KEY = 'LHId46114Z1J3zwAggIwATTZ6CyWM1BpVAR4jZD3'

#Register the app with Parse Server
register(APPLICATION_ID, REST_API_KEY, master_key=MASTER_KEY)


TOKEN = "1204379924:AAFToKOG3WVdLETDM-TyV0Rtl2h6o1SrNIs"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Hello. Welcome to SIH Notification Bot. Please send your email id registered with the DB to add your id for notifications.")

def reply(message):
    bot.reply_to(message, "Thanks for registering with us. You'll get further notifications from us.")

def saveIdToDB(message,user_email):
    saveContact = Function("saveContactDetails")
    result = saveContact(email=user_email, user_id=message.from_user.id)
    print(result)
    if(result['result'] == "Success"):
        reply(message)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    saveIdToDB(message,message.text)
    
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://sih-telegram-bot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))