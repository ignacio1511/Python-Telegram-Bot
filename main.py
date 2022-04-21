## Import model 
from operator import imod

from prompt_toolkit import HTML
from model import NeuralNet

#Import functions
from functions import normalize,tokenize,stem,bag_of_words,sendText,scheduleNutrition,scheduleMotivation

##Import sheets variables
from sheets import motivation, nutrition

##Import menus and keyboards
from navigation import main_menu,first_menu,second_menu,third_menu,second_submenu,error,main_menu_keyboard,first_menu_keyboard,second_menu_keyboard,third_menu_keyboard,main_menu_message,first_menu_message,second_menu_message,third_menu_message

## Import libraries
import requests
import random
import telegram
import os
import logging
import requests
import telegram 
from schedule import every, repeat, run_pending
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
import logging
from typing import Dict
from turtle import up, update, xcor
import torch
import json
import numpy as np
from telegram import Update
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,CallbackContext,CallbackQueryHandler
#nltk.download('punkt')



with open('intents.json', 'r') as f:
    intents = json.load(f)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
FILE = "databot.pth"
data = torch.load(FILE)
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
palabras_totales = data["palabras_totales"]
tags = data["tags"]
model_state = data["model_state"]
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()
bot_name = "Seiken"
respuestas = ["Me alegro", "Genial crack", "Vale bro", "Chevere crack, algo más?"]
mensaje_motivacion=" "
mensaje_alimentacion=" "
contador_pasos=0
logging.basicConfig(level=logging.INFO, format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()
TOKEN = os.getenv("BOT TOKEN")


def start(update: Update, context: CallbackContext):
    tipo=update.effective_chat['type']
    if tipo == "supergroup":
        pass ##solo responde a mensajes en privado
    name = update.effective_user['first_name']
    update.message.reply_text(f"Hola {name} 👋  Soy SEIKEN, un guerrero como tu 💪🏻🔥 Estoy aquí para ayudarte.")
    update.message.reply_text(main_menu_message(),
                        reply_markup=main_menu_keyboard())

def echo(update: Update, context: CallbackContext):
    tipo=update.effective_chat['type']
    print("UPDATE ..." + str(update))
    print("CONTEXT ... " + str(context))
    print(tipo)
    if tipo =="private":
        user_id=update.effective_user['id']
        name = update.effective_user['first_name']
        text = update.message.text
        sentence = text
        logger.info(f"El usuario {name} {user_id} mandó: {[sentence]}")

        sentence = tokenize(sentence)
        x = bag_of_words(sentence,palabras_totales)
        x = x.reshape(1,x.shape[0])
        x = torch.from_numpy(x).to(device)

        output = model(x)
        _, predicted = torch.max(output,dim=1)
        tag = tags[predicted.item()]

        probs = torch.softmax(output,dim = 1)
        prob = probs[0][predicted.item()]

        if prob.item() > 0.75:
            for intent in intents["intents"]:
                if tag == intent["tag"]:
                    context.bot.sendMessage(
                        chat_id=user_id,
                        parse_mode = "MarkdownV2",
                        text = f"{random.choice(intent['responses'])} "
                    )
        else:
            context.bot.sendMessage(
                chat_id=user_id,
                parse_mode = "MarkdownV2",
                text = f"{random.choice(respuestas)}"
            )


if __name__== "__main__":
    my_bot = telegram.Bot(token="BOT TOKEN")


scheduler_motivation = BackgroundScheduler()
scheduler_nutrition = BackgroundScheduler()
updater=Updater(my_bot.token, use_context=True)

#Creando un despachador
dp=updater.dispatcher

#Creando los manejadores
dp.add_handler(CommandHandler("start",start))
dp.add_handler(MessageHandler(Filters.text, echo))
updater.dispatcher.add_error_handler(error)

scheduler_nutrition.add_job(scheduleNutrition,'interval', hours=24, start_date='2022-04-21 05:58:00', end_date='2022-05-26 06:05:00')
scheduler_nutrition.add_executor
scheduler_motivation.add_job(scheduleMotivation,'interval', hours=24, start_date='2022-04-21 05:58:00', end_date='2022-05-26 06:05:00')
scheduler_motivation.add_executor

#### MENUS #####
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
updater.dispatcher.add_handler(CallbackQueryHandler(third_menu, pattern='m3'))

updater.start_polling()
print("BOT LISTO")
updater.idle()
