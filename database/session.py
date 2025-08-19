import sqlalchemy as sq
from models import Base, Word, User, UserWord
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
    echo=True,
)

Session = sessionmaker(bind=engine)


def create_tables():
    Base.metadata.drop_all(engine)  # later delete / comment
    Base.metadata.create_all(engine)


'''loading start pack of words'''


def load_initial_words():

    with open('database/initial_words.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    with Session.begin() as session:
        for word in data:
            session.add(
                Word(
                    original_word=word['original_word'],
                    translate_word=word['translate_word'],
                    status='initial_pack'
                )
            )


'''adding new user if it is not exists in bd'''


def add_new_user(user_id):
    with Session.begin() as session:

        if user_id.isdigit():
            user_id = str(user_id)

        filter_user = User.user_id == user_id
        new_user = session.query(User).filter(filter_user).one_or_none()

        if not new_user:
            session.add(
                User(
                    user_id=user_id,
                    name_user='name'
                )
            )


'''adding start pack of words for new user'''


def add_initial_words_for_user(user_id):
    with Session.begin() as session:

        filter_words = Word.status == 'initial_pack'
        initial_words = session.query(Word).filter(filter_words).all()

        for word in initial_words:
            session.add(
                UserWord(
                    word_id=word.word_id,
                    user_id=user_id
                )
            )


''''''


def add_new_word_for_user(word, user_id):
    with Session.begin() as session:

        filter_words = Word.status == 'initial_pack'
        initial_words = session.query(Word).filter(filter_words).all()

        for word in initial_words:
            session.add(
                UserWord(
                    word_id=word.word_id,
                    user_id=user_id
                )
            )


# how to check if tables doesnt exist - then create once and then forget about that
if __name__ == "__main__":
    create_tables()

    load_initial_words()

    add_new_user('1')

    add_initial_words_for_user('1')
