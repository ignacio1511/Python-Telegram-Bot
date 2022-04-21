import nltk
from nltk.stem import SnowballStemmer
import numpy as np

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
