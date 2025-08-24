from database.session import create_tables, load_initial_words
from bot import bot
from utils.logger import main_logger


logger = main_logger(__name__)


if __name__ == '__main__':

    create_tables()  # создание таблиц
    load_initial_words()  # добавление стартового набора слов

    # запуск бота
    while True:
        try:
            bot.polling(non_stop=True, timeout=60)
        except Exception as e:
            logger.error(f'Ошибка при запуске бота: {e}')
