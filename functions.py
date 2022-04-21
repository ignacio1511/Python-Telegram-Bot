import nltk
from nltk.stem import SnowballStemmer
import numpy as np
from prompt_toolkit import HTML
import requests
import random
from sheets import motivation,nutrition

telegramUrl = 'http://api.telegram.org/bot'
bot_token = '5126043917:AAH1AlfvaOhFJuf2nBdEI8FhuUa79nc1Z18'
telegramAPI = telegramUrl + bot_token


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


stemmer = SnowballStemmer('spanish')


def tokenize(frase):
    return nltk.word_tokenize(frase)


def stem(palabra):
    return normalize(stemmer.stem(palabra.lower()))


def bag_of_words(tokenized_sentence, words):
    sentence_words = [stem(word) for word in tokenized_sentence]
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1

    return bag


def sendText(chat_id,mensaje):
    base_url =  telegramAPI +'/sendMessage?chat_id=' + chat_id + '&text="{}"'.format(mensaje)
    return requests.get(base_url)

  
def scheduleMotivation():
    mensaje = random.choice(motivation)
    sendText('394714808',mensaje)

def scheduleNutrition():
    mensaje = random.choice(nutrition)
    sendText('394714808',mensaje)