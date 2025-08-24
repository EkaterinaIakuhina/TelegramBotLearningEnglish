from telebot import TeleBot, types
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup
import random
from utils.logger import main_logger
from database.session import add_new_user, add_new_word_for_user, del_word_for_user, get_users_words, \
    add_initial_words_for_user, get_user_id, change_status_to_deleting, change_status_to_adding, change_status_to_guessing, get_user_status
from utils.translator import get_translation

logger = main_logger(__name__)

BOT_TOKEN = '8053098189:AAGHRT2JgTP6DA4P9vG1rtKmE3ySQtGp1DU'

state_storage = StateMemoryStorage()
bot = TeleBot(BOT_TOKEN, state_storage=state_storage)

bot_commands = {
    'start': 'Это бот по изучению слов на английском языке.\n'
    'Напечатай /help, чтобы увидеть все возможные команды',
    'help': 'Бот сам переводит слова, тебе нужно только добавить слово на русском в список изучаемых слов.\n\n'
            'Ты можежь начать угадывать слово: /word\n'
            'Ты можешь добавить новое слово: /add \n'
            'Ты можешь удалить слово из изучаемых: /del \n'
            'Ты можешь вывести все слова, которые сейчас изучаешь: /ls \n',
    'add': 'Напиши слово на русском и нажми отправить \n'
            'Чтобы закончить добавление слов нажми команду /stop',
    'del': 'Напиши слово на русском и нажми отправить, слово и его перевод удалятся из твоего списка \n'
            'Чтобы закончить удаление слов нажми команду /stop',
    'ls': 'Присылаю список всех твоих слов:'
}


class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    other_words = State()
    all_words = State()


class CommandBtn:
    ADD_WORD = 'Добавить слово'
    DELETE_WORD = 'Удалить слово'
    NEXT = 'Дальше'
    ALL_WORD = 'Вывести список слов'


def send_target_word(message, name_user, user_words):

    keybord = types.ReplyKeyboardMarkup(row_width=2)

    # получаем все слова пользователя
    ru_words = [word[0] for word in user_words]
    en_words = [word[1] for word in user_words]
    words_dict = dict(zip(ru_words, en_words))

    # устанавливаем случайное слово для угадывания
    target_word = random.choice(ru_words)
    target_word_translate = words_dict[target_word]
    other_words = en_words
    other_words.remove(target_word_translate)

    # создание клавиатуры для слов
    target_word_button = types.KeyboardButton(target_word_translate)
    other_words_button = [types.KeyboardButton(
        w) for w in random.sample(other_words, 3)]
    buttons = [target_word_button] + other_words_button
    random.shuffle(buttons)

    # добавление доп.кнопок для управления
    add_word_button = types.KeyboardButton(CommandBtn.ADD_WORD)
    del_word_button = types.KeyboardButton(CommandBtn.DELETE_WORD)
    next_button = types.KeyboardButton(CommandBtn.NEXT)
    all_words_button = types.KeyboardButton(CommandBtn.ALL_WORD)

    buttons.extend([next_button, add_word_button, del_word_button,
                    all_words_button])

    keybord.add(*buttons)

    # отправление слова для угадывания
    try:
        bot.send_message(name_user, target_word, reply_markup=keybord)
    except Exception as e:
        logger.error(
            f'Пользователь {name_user}. Произошла ошибка при отправке слова: {e}')

    # запоминания слова-его перевода
    bot.set_state(message.from_user.id, MyStates.target_word, name_user)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['target_word'] = target_word
        data['translate_word'] = target_word_translate
        data['other_words'] = other_words


@bot.message_handler(commands=['start'])
def send_start_message(message):
    '''отправляет приветственное сообщение
    добавляет пользователя в бд и присваивает ему стартовый набор слов, если его еще нет в бд
    и сразу же начинает взаимодействие
    '''
    name_user = message.chat.id
    bot.send_message(name_user, bot_commands['start'])

    user_id = get_user_id(name_user=name_user)

    if not user_id:
        add_new_user(name_user)
        logger.info(f'Добавление пользователя: {name_user}')
        add_initial_words_for_user(name_user)

    user_words = get_users_words(name_user)

    bot.send_message(name_user, 'Какой перевод для слова:')
    send_target_word(message, name_user, user_words)


@bot.message_handler(func=lambda message: message.text == CommandBtn.NEXT)
@bot.message_handler(commands=['word'])
def send_next_target_word(message):
    'отправка нового слова для угадывания при нажатии кнопки или выборе команды'
    name_user = message.chat.id
    change_status_to_guessing(name_user)

    user_words = get_users_words(name_user)
    send_target_word(message, name_user, user_words)


@bot.message_handler(commands=['help'])
def send_help(message):
    'отправляет сообщение, что бот может делать'
    bot.send_message(message.chat.id, bot_commands['help'])


@bot.message_handler(commands=['stop'])
def stop_action(message):
    'останавливает добавление или удаление слов и продолжает угадавание слов'
    name_user = message.chat.id
    change_status_to_guessing(name_user)

    bot.send_message(name_user, 'Возвращаюсь к угадыванию слов')

    user_words = get_users_words(name_user)
    send_target_word(message, name_user, user_words)


@bot.message_handler(commands=['ls'])
@bot.message_handler(func=lambda message: message.text == CommandBtn.ALL_WORD)
def request_for_all_words(message):
    'отправляет пользователю список всех его слов при нажатии кнопки или выборе команды'
    name_user = message.chat.id
    list_of_words = get_users_words(name_user)

    try:
        if not list_of_words:
            bot.send_message(name_user, 'Список слов пока пуст.')
        else:
            bot.send_message(
                name_user, f'В твоем списке {len(list_of_words)} слов.')

            for num, word in enumerate(list_of_words, start=1):
                bot.send_message(
                    name_user, f'{num}: {word[0]} - {word[1]}')
    except Exception as e:
        logger.error(f'Ошибка при выводе списка всех слов: {e}')


@bot.message_handler(commands=['del'])
@bot.message_handler(func=lambda message: message.text == CommandBtn.DELETE_WORD)
def request_for_delete(message):
    'начинает операцию по удалению слов'
    name_user = message.chat.id
    bot.send_message(name_user, bot_commands['del'])
    change_status_to_deleting(name_user)


@bot.message_handler(func=lambda message: get_user_status(message.chat.id) == 'deleting')
def delete_words(message):
    'удаляет указанное пользователем слово или говорит, что такого не существует'
    name_user = message.chat.id

    word = message.text.capitalize()

    result = del_word_for_user(word, name_user)

    if not result:
        logger.warning(
            f'Пользователь {name_user}, удаление несуществующего слова')
        bot.send_message(
            name_user, f'Слова {word} нет в твоем списке или некорректно введено слово. Попробуй еще.')
    else:
        logger.info(f'Пользователь {name_user}, слово {word} успешно удалено')
        bot.send_message(
            name_user, f'Слово {word} удалено из твоего списка.')
        bot.send_message(name_user, 'Для остановки нажми /stop')


@bot.message_handler(commands=['add'])
@bot.message_handler(func=lambda message: message.text == CommandBtn.ADD_WORD)
def request_for_add(message):
    'начинает операцию по добавлению слов'
    name_user = message.chat.id
    bot.send_message(name_user, bot_commands['add'])
    change_status_to_adding(name_user)


@bot.message_handler(func=lambda message: get_user_status(message.chat.id) == 'adding')
def add_words(message):
    'добавляет слова в бд, указанные пользователем и его перевод на английский и выводит сообщение об этом'
    name_user = message.chat.id

    word = message.text.capitalize()
    translated_word = get_translation(word)

    if not translated_word:
        logger.warning(
            f'Пользователь {name_user}, добавление слова, для которого не существует перевода.')
        bot.send_message(
            name_user, f'Слова {word} не существует. Нет ли ошибки?')
    else:
        logger.info(
            f'Пользователь {name_user}, слово {word} успешно добавлено с переводом {translated_word}')
        add_new_word_for_user(word, translated_word, name_user)
        bot.send_message(
            name_user, f'Слово добавлено. Перевод: {translated_word}')
        bot.send_message(name_user, 'Для остановки нажми /stop')

        list_of_words = get_users_words(name_user)
        bot.send_message(
            name_user, f'В твоем списоке {len(list_of_words)} слов.')


@bot.message_handler(func=lambda message: get_user_status(message.chat.id) == 'guessing')
def checking_guessing(message):
    # проверка слов происходит постоянно, если пользователь не в статусе "добавления слова" / "удаление слова"
    guess = message.text
    name_user = message.chat.id

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_word_translate = data['translate_word']
        target_word = data['target_word']

    if guess == target_word_translate:
        bot.reply_to(message, f'Правильно. {target_word} - {guess}')
    else:
        bot.reply_to(message, f'Неверно. Попробуй еще.')
        logger.info(f'Пользователь {name_user}, '
                    f'Неверная попытка угадывания (слово: {target_word}, попытка: {guess}, правильно: {target_word_translate})')
