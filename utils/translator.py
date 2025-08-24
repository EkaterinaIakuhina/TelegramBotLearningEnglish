from utils.logger import main_logger
from yandexfreetranslate import YandexFreeTranslate

yt = YandexFreeTranslate(api="ios")
logger = main_logger(__name__)


def get_translation(word: str) -> str | None:
    '''возвращает перевод слова с русского на английский или None, если слово введено неверное.'''
    logger.info(f'Перевод слова')
    try:
        translation = yt.translate(
            "ru",
            "en",
            word
        )
    
        if translation == word:
            logger.error(f"Ошибка при переводе слова: {e}")
            return None
        
        return translation
    
    except Exception as e:
        logger.error(f"Ошибка при переводе слова: {e}")

