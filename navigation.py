from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

def main_menu(bot, update: Update):
  bot.callback_query.message.edit_text(main_menu_message(),
                          reply_markup=main_menu_keyboard())

def first_menu(bot, update: Update):
  bot.callback_query.message.edit_text(first_menu_message(),
                          reply_markup=first_menu_keyboard())

def second_menu(bot, update: Update):
  bot.callback_query.message.edit_text(second_menu_message(),
                          reply_markup=second_menu_keyboard())

def third_menu(bot, update: Update):
  bot.callback_query.message.edit_text(third_menu_message(),
                          reply_markup=third_menu_keyboard())

def second_submenu(bot, update: Update):
  pass


def error(update, context: CallbackContext):
    print(f'Update {update} caused error {context.error}')

############################ Keyboards #########################################
def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton(text = 'Rutinas Reto Seiken', callback_data='m1')],
              [InlineKeyboardButton('Alimentacion Seiken', callback_data='m2')],
              [InlineKeyboardButton('Chequeos', callback_data='m3')]]
  return InlineKeyboardMarkup(keyboard)

def first_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Nivel 1: Ningun requisito', url = 'https://drive.google.com/file/d/1dWD-vG1tPFBVSXtwloLjnrQHB2BAGGh5/view?usp=sharing' ,callback_data='m1_1', )],
              [InlineKeyboardButton('Nivel 2: +15 planchas elevadas', url='https://drive.google.com/file/d/11ERS7V1iGdQ7oAuNL3lsRIwO27JIKmdn/view?usp=sharing', callback_data='m1_2')],
              [InlineKeyboardButton('Nivel 3: + 5 planchas una mano', url = 'https://drive.google.com/file/d/1o-pEmd0noGLYynsbF4LN5hlq4jtoBqlt/view?usp=sharing', callback_data='main')],
              [InlineKeyboardButton('Guia de ejercicios alternativos', url = 'https://drive.google.com/file/d/1WZwtwh1xvsHXuJ9JtFtVUcWxOXSlWJoF/view?usp=sharing', callback_data='main')],
              [InlineKeyboardButton('Inicio', callback_data='main')]]
              
  return InlineKeyboardMarkup(keyboard)

def second_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Aprende sobre el Ayuno Seiken', url = 'https://d2saw6je89goi1.cloudfront.net/uploads/digital_asset/file/950568/Los_Secretos_del_Ayuno_Seiken__1__compressed.pdf', callback_data='m2_1')],
              [InlineKeyboardButton('Calculador de calorías', url = 'https://www.calculator.net/calorie-calculator.html', callback_data='m2_2')],
              [InlineKeyboardButton('Inicio', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)


def third_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Calendario de chequeos', url = 'https://d2saw6je89goi1.cloudfront.net/uploads/digital_asset/file/984964/SeikenMB_-_Chequeos__1_.png', callback_data='m3_1')],
              [InlineKeyboardButton('Registra tu progreso (chequeos quincenales)', url = 'https://forms.gle/ZCotB7TLspT8f1vQ7' , callback_data='m3_2')],
              [InlineKeyboardButton('Inicio', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

#########################################################################
def main_menu_message():
  return f"Para comenzar, escribe /start"

def first_menu_message():
    return 'Elige el nivel con el que te sientas más cómodo. Cada persona tiene un progreso diferente y el momento de pasar al siguiente nivel es cuando te sientes demasiado cómodo con los ejercicios.'
#   return 'Escoge el nivel con el que te sientas más cómodo \n \n🔥 Nivel 1 - Soy un Seiken iniciando con todo' + '\n \n🔥🔥 Nivel 2 - Puedo hacer +10  planchas en elevación y 5 dominadas supinas \n \n🔥🔥🔥 Nivel 3 - Puedo hacer +5 planchas con una mano y +10 dominadas'

def second_menu_message():
  return 'Esta seccion es para ayudarte a tener una alimentación correcta y saludable'


def third_menu_message():
  return '🚨 Para formar parte de los posibles ganadores, debes realizar los 5 chequeos 🚨'

###########