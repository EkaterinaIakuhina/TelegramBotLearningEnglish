from telebot import TeleBot, types
import random
from logger import main_logger
import os
import dotenv

'''initializing logger '''
logger = main_logger(__name__)
dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = TeleBot(BOT_TOKEN)

bot_commands = {
    'start': 'Это бот по изучению слов на английском языке. '
    'Напечатай /help, что увидеть все возможные команды',
    'help': 'Бот сам переводит слова, тебе нужно только добавить слово на русском в список изучаемых слов. '
            'Ты можешь добавить новое слово: /add '
            'Ты можешь удалить слово из изучаемых: /del '
            'Ты можешь вывести все слова, которые сейчас изучаешь: /ls ',
    'add': 'Напиши слово на русском и нажми отправить',
    'del': 'Напиши слово на русском и нажми отправить, слово и его перевод удалятся из твоего списка',
    'ls': 'Присылаю список всех твоих слов:'
}


'''creating keyboard for words to translate'''
word1 = types.KeyboardButton('word1')
word2 = types.KeyboardButton('word2')
word3 = types.KeyboardButton('word3')
word4 = types.KeyboardButton('word4')

keybord = types.ReplyKeyboardMarkup(row_width=2)
keybord.add(word1, word2, word3, word4)


'''sending this keyboard'''


@bot.message_handler(commands=['start'])
def send_words(message):
    bot.send_message(message.chat.id, bot_commands['start'])


@bot.message_handler(commands=['help'])
def send_words(message):
    bot.send_message(message.chat.id, bot_commands['help'])


'''здесь нужен селект запрос к базе данных по id пользователя, проверка, есть ли айди
если слово никакие еще не добавлялось, айди нет -> вывести "у вас пока нет слов"'''


@bot.message_handler(commands=['ls'])
def send_words(message):
    bot.send_message(message.chat.id, bot_commands['help'])


'''checking the answer
there will be process: if right - then 
'''


@bot.message_handler(func=lambda message: True)
def check_answer(message):
    if message.text == 'right result':
        bot.reply_to(message, 'Правильный ответ!')
