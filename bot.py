from telebot import TeleBot, types
import random
from logger import main_logger

'''initializing looger '''
logger = main_logger()

bot = TeleBot(TOKEN)

'''creating keyboard for words to translate'''
word1 = types.KeyboardButton('word1')
word2 = types.KeyboardButton('word2')
word3 = types.KeyboardButton('word3')
word4 = types.KeyboardButton('word4')

keybord = types.ReplyKeyboardMarkup(row_width=2)
keybord.add(word1, word2, word3, word4)


'''sending this keyboard'''
@bot.message_handler(commands=['start', 'new_word'])
def send_words(message):
    bot.send_message(message.chat.id, 'smth', reply_markup=keybord)


'''checking the answer
there will be process: if right - then 
'''
@bot.message_handler(func=lambda message: True)
def check_answer(message):
    if message.text ==  'right result':
        bot.reply_to(message, 'Правильный ответ!')

    
    

