from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import declarative_base, relationship
import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name_user = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    status = Column(String(30), default='guessing')

    words = relationship("UserWord", back_populates="user")

    def __repr__(self):
        return f'User: chat_id = {self.user_id}'


class Word(Base):
    __tablename__ = 'words'

    word_id = Column(Integer, primary_key=True)
    original_word = Column(String(length=60), nullable=False)
    translate_word = Column(String(length=60), nullable=False)
    language_from = Column(String(length=40), default='ru')
    language_to = Column(String(length=40), default='en')
    status = Column(String(length=20), default=None)

    users = relationship("UserWord", back_populates="word")

    def __repr__(self):
        return f'Word {self.word_id} ({self.original_word}:{self.translate_word})'


class UserWord(Base):
    __tablename__ = 'user_words'

    id = Column(Integer, primary_key=True)
    word_id = Column(Integer,  ForeignKey('words.word_id'), nullable=False)
    user_id = Column(Integer,  ForeignKey('users.user_id'), nullable=False)

    user = relationship("User", back_populates="words")
    word = relationship("Word", back_populates="users")

    def __repr__(self):
        return f'{self.id}: User with {self.user_id} has word {self.word_id}'
