## Import model 
from operator import imod
from model import NeuralNet

#Import functions
from functions import normalize,tokenize,stem,bag_of_words

##Import sheets variables
from sheets import mensajes__motivacion_mañana,tips_alimentacion, trigger_mañana, trigger_tarde,trigger_noche

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
from turtle import update, xcor
import torch
import json
import numpy as np
from telegram import Update
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,CallbackContext,CallbackQueryHandler
#nltk.download('punkt')

"""
Paso 1: Grupo de Telegram en donde se mandarán los mensajes https://t.me/+MZ6A91jsC_o1ZWIx
Paso 2: Crear Telegram Bot
Paso 3: Chat ID (-1001621138106)
Paso 4: API Bot http://api.telegram.org/bot5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0/getUpdates
Paso 5: Mandar mensaje http://api.telegram.org/bot5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0/sendMessage?chat_id=-628790056&text="Mensaje prueba"

"""


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as f:
    intents = json.load(f)

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
contador_pasos=54

logging.basicConfig(level=logging.INFO, format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()


TOKEN = os.getenv("5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0")

def start(update: Update, context: CallbackContext):
    tipo=update.effective_chat['type']

    if tipo == "supergroup":
        pass

    name = update.effective_user['first_name']
    update.message.reply_text(f"Hola {name} 👋  Soy SEIKEN, un guerrero como tu 💪🏻🔥 Estoy aquí para ayudarte.")
    update.message.reply_text(main_menu_message(),
                        reply_markup=main_menu_keyboard())


def echo(update: Update, context: CallbackContext):
    tipo=update.effective_chat['type']
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



def envio_motivacion_mañana():
    global mensaje_motivacion
    mensaje_elegido = random.choice(mensajes__motivacion_mañana)

    while mensaje_elegido == mensaje_motivacion or mensaje_elegido == "motivacion_mañana":
        mensaje_elegido = random.choice(mensaje_elegido)

    base_url = 'http://api.telegram.org/bot5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0/sendMessage?chat_id=-1001621138106&text="{}"'.format(mensaje_elegido)
    return requests.get(base_url)
    
def envio_tips_alimentacion():
    global mensaje_alimentacion
    mensaje_elegido = random.choice(tips_alimentacion)
    while mensaje_elegido == mensaje_alimentacion or mensaje_elegido == "alimentacion_tarde":
        mensaje_elegido = random.choice(tips_alimentacion)
        
    base_url = 'http://api.telegram.org/bot5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0/sendMessage?chat_id=-1001621138106&text="{}"'.format(mensaje_elegido)
    mensaje_alimentacion=mensaje_elegido
    return requests.get(base_url) 

mensaje_trigger_mañana = " "
    
mensaje_trigger_mañana = ""
def envio_trigger_mañana():
    global mensaje_trigger_mañana
    mensaje_elegido = random.choice(trigger_mañana)
    while mensaje_elegido == mensaje_trigger_mañana or mensaje_elegido == "trigger_mañana":
        mensaje_elegido = random.choice(trigger_mañana)
        
    base_url = 'http://api.telegram.org/bot5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0/sendMessage?chat_id=-1001621138106&text="{}"'.format(mensaje_elegido)
    mensaje_trigger_mañana=mensaje_elegido
    return requests.get(base_url) 


mensaje_trigger_tarde = ""
def envio_trigger_tarde():
    global mensaje_trigger_tarde
    mensaje_elegido = random.choice(trigger_tarde)
    while mensaje_elegido == mensaje_trigger_tarde or mensaje_elegido == "trigger_tarde":
        mensaje_elegido = random.choice(trigger_tarde)
        
    base_url = 'http://api.telegram.org/bot5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0/sendMessage?chat_id=-1001621138106&text="{}"'.format(mensaje_elegido)
    mensaje_trigger_tarde=mensaje_elegido
    return requests.get(base_url) 


mensaje_trigger_noche = ""
def envio_trigger_noche():
    global mensaje_trigger_noche
    mensaje_elegido = random.choice(trigger_noche)
    while mensaje_elegido == mensaje_trigger_noche or mensaje_elegido == "trigger_noche":
        mensaje_elegido = random.choice(trigger_noche)

    mensaje_trigger_noche = mensaje_elegido
        
    base_url = 'http://api.telegram.org/bot5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0/sendMessage?chat_id=-1001621138106&text="{}"'.format(mensaje_elegido)
    return requests.get(base_url) 


def envio_chequeo_quincenal():
    chequeo_quincenal = '🚨 IMPORTANTE 🚨' + '\n' + 'Hoy es día de CHEQUEO. Sube tu progreso aquí' + '\n' + '👉🏻 https://forms.gle/ZCotB7TLspT8f1vQ7 👈🏻'
    base_url = 'http://api.telegram.org/bot5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0/sendMessage?chat_id=-1001621138106&text="{}"'.format((chequeo_quincenal))
    return requests.get(base_url) 


def envio_pasos_diarios(): 
    global contador_pasos
    pasos_diarios = [ ]

    for j in range(1000,20000,320):
        pasos_diarios.append(j)

    pasos_diarios.pop()
    pasos_diarios.append(20000)
    base_url = 'http://api.telegram.org/bot5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0/sendMessage?chat_id=-1001621138106&text="{}"'.format(((f"El objetivo de pasos de hoy es: 🔥 {[pasos_diarios[contador_pasos]]}🔥 ")))
    contador_pasos = contador_pasos + 1
    return requests.get(base_url)

envio_motivacion_mañana()

def mensajes_bienvenida(update,context):
    bot=context.bot
    chatID=update.message.chat_id
    print(chatID)
    updateMsg= getattr(update,"message",None)
    for user in updateMsg.new_chat_members:
        username=user.first_name

    logger.info(f'El usuario {username} ha ingresado al grupo')

    mensajes_bienvenida = [ f'Bienvenido al Reto Seiken 2022, {username}. Vamos a darle con todo bro 💪🏻🔥', 
    f'Hola {username}, bienvenido', 
    f'¡{username}! Bienvenido bro, un gusto que estés aquí',
    f'Hola {username}, bienvenido al Reto Seiken 2022, estamos seguros de que podrás tener los cambios que estás buscando. A darle',
    f'Bienvenido a la comunidad Seiken, {username}',
    f'Hola {username}, bienvenido. Estamos aquí para lo que necesites',
    f"Hola {username}, que gusto tenerte aquí. Cada día vmaos creciendo más esta comunidad 💪🏻🔥"]

    bot.sendMessage(
        chat_id=chatID,
        parse_mode="HTML",
        text= random.choice(mensajes_bienvenida)
    )

scheduler1 = BackgroundScheduler()
scheduler2 = BackgroundScheduler()
scheduler3 = BackgroundScheduler()
scheduler4 = BackgroundScheduler()

### TRIGGERS ###
scheduler5 = BackgroundScheduler()
scheduler6 = BackgroundScheduler()
scheduler7 = BackgroundScheduler()

### MAIN ### 

if __name__== "__main__":
    my_bot = telegram.Bot(token="5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0")
    print(my_bot.getMe())
    scheduler1.add_job(envio_tips_alimentacion, 'interval', hours=24, start_date='2022-01-30 15:00:00', end_date='2022-03-26 11:55:00') #10 AM
    scheduler1.start()
    scheduler2.add_job(envio_motivacion_mañana, 'interval', hours=24, start_date='2022-01-30 13:30:00', end_date='2022-03-26 7:00:00') #8:30AM
    scheduler2.start()
    scheduler3.add_job(envio_chequeo_quincenal, 'interval', days=15, start_date='2022-01-24 11:00:00', end_date='2022-03-26 05:05:00')
    scheduler3.start()
    scheduler4.add_job(envio_pasos_diarios, 'interval', hours=24, start_date='2022-01-30 11:10:00', end_date='2022-03-26 06:05:00') #6AM
    scheduler4.start()
    scheduler5.add_job(envio_trigger_mañana, 'interval', hours=24, start_date='2022-01-30 12:00:00', end_date='2022-03-26 06:05:00') #7AM
    scheduler5.start()
    scheduler6.add_job(envio_trigger_tarde, 'interval', hours=24, start_date='2022-01-30 18:10:00', end_date='2022-03-26 06:05:00') #1:10PM
    scheduler6.start()
    scheduler7.add_job(envio_trigger_noche, 'interval', hours=24, start_date='2022-01-30 02:10:00', end_date='2022-03-26 06:05:00') #9:10PM
    scheduler7.start()

updater=Updater(my_bot.token, use_context=True)

#Creando un despachador
dp=updater.dispatcher

#Creando los manejadores
dp.add_handler(CommandHandler("start",start))
dp.add_handler(MessageHandler(Filters.text, echo))
dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,mensajes_bienvenida))
updater.dispatcher.add_error_handler(error)

#### MENUS #####
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
updater.dispatcher.add_handler(CallbackQueryHandler(third_menu, pattern='m3'))

updater.start_polling()
print("BOT LISTO")
updater.idle()
