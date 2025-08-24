import sqlalchemy as sq
from database.models import Base, Word, User, UserWord
from sqlalchemy.orm import sessionmaker
import json
import dotenv
import os

dotenv.load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


DSN = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = sq.create_engine(
    url=DSN,
)

Session = sessionmaker(bind=engine)


def create_tables():
    Base.metadata.drop_all(engine)  # later delete / comment
    Base.metadata.create_all(engine)


def load_initial_words():
    '''  функция добавляет стартовый набор слов в бд '''
    with open('database/initial_words.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    with Session.begin() as session:

        check_query = sq.select(Word).limit(1)
        result = session.execute(check_query).scalars().all()

        if not result:

            for word in data:
                session.add(
                    Word(
                        original_word=word['original_word'],
                        translate_word=word['translate_word'],
                        status='initial_pack'
                    )
                )


def get_user_id(name_user: int) -> int:
    ''' возвращает user_id пользователя или 0, если его нет в бд '''
    with Session.begin() as session:

        query = sq.select(User.user_id).where(User.name_user == name_user)
        user_id = session.execute(query).scalars().one_or_none()

        return user_id


def add_new_user(name_user: int) -> None:
    ''' функция добавляет в бд нового пользователя '''
    with Session.begin() as session:

        new_user = get_users_words(name_user)

        if not new_user:
            session.add(
                User(
                    name_user=name_user
                )
            )


def add_initial_words_for_user(name_user: int) -> None:
    ''' функция добавляет новому пользователя стартовый пакет слов '''
    with Session.begin() as session:

        word_query = sq.select(Word.word_id)\
            .where(Word.status == 'initial_pack')
        initial_words = session.execute(word_query).scalars().all()

        user_query = sq.select(User.user_id).where(User.name_user == name_user)
        user_id = session.execute(user_query).scalars().first()

        for word in initial_words:
            session.add(
                UserWord(
                    word_id=word,
                    user_id=user_id
                )
            )


def add_new_word_for_user(word: str, translate_word: str, name_user: int) -> None:
    ''' функция добавляет новое слово и его перевод для пользователя в бд '''
    with Session.begin() as session:

        word_query = sq.select(Word.word_id).where(Word.original_word == word)
        word_id = session.execute(word_query).scalars().first()

        if not word_id:

            stmt = sq.insert(Word).values(
                original_word=word,
                translate_word=translate_word
            )

            result = session.execute(stmt)
            word_id = result.inserted_primary_key[0]

        user_query = sq.select(User.user_id).where(User.name_user == name_user)
        user_id = session.execute(user_query).scalars().first()

        add_word_to_users_stmt = sq.insert(UserWord)\
            .values(
                word_id=word_id,
                user_id=user_id
        )

        session.execute(add_word_to_users_stmt)

# def get_words(w


def del_word_for_user(word: str, name_user: int) -> int:
    '''  функция возвращает количество удаленных строк '''
    with Session.begin() as session:

        word_query = sq.select(Word.word_id).where(Word.original_word == word)
        word_id = session.execute(word_query).scalars().first()

        user_query = sq.select(User.user_id).where(User.name_user == name_user)
        user_id = session.execute(user_query).scalars().first()

        delete_stmt = sq.delete(UserWord)\
            .where(UserWord.word_id == word_id, UserWord.user_id == user_id)
        delete_result = session.execute(delete_stmt)

        return delete_result.rowcount


def get_users_words(name_user: int) -> list[tuple]:
    ''' функция возвращает список кортежей (слово, перевод) или пустой список '''
    with Session() as session:

        query = (sq.select(Word.original_word, Word.translate_word)
                 .join(UserWord, Word.word_id == UserWord.word_id)
                 .join(User, User.user_id == UserWord.user_id)
                 .where(User.name_user == name_user)
                 )

        user_words = session.execute(query).all()
        session.commit()

        return user_words


def change_status_to_adding(name_user: int) -> None:
    ''' функция изменяет статус пользователя для добавления слов'''
    with Session.begin() as session:

        update_st = sq.update(User).where(
            User.name_user == name_user).values(status='adding')

        session.execute(update_st)


def change_status_to_deleting(name_user: int) -> None:
    ''' функция изменяет статус пользователя для удаления слов'''
    with Session.begin() as session:

        update_st = sq.update(User).where(
            User.name_user == name_user).values(status='deleting')

        session.execute(update_st)


def change_status_to_guessing(name_user: int) -> None:
    ''' функция изменяет статус пользователя для угадывания перевода'''
    with Session.begin() as session:

        update_st = sq.update(User).where(
            User.name_user == name_user).values(status='guessing')

        session.execute(update_st)


def get_user_status(name_user: int) -> str:
    '''возвращает текущий статус пользователя'''
    with Session.begin() as session:

        request = sq.select(User.status).where(User.name_user == name_user)

        status = session.execute(request).scalars().one_or_none()

        return status
