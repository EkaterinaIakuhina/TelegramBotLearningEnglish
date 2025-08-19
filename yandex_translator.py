from logger import main_logger
from yandexfreetranslate import YandexFreeTranslate

yt = YandexFreeTranslate(api="ios")
logger = main_logger(__name__)


def get_translation(word):
    logger.info(f'Перевод слова')
    try:
        translation = yt.translate(
            "ru",
            "en",
            word
        )
        return translation

    except Exception as e:
        logger.error(f"Ошибка при переводе слова: {e}")

