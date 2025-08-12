import sqlalchemy as sq 
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    user_id = sq.Column(sq.Integer, primary_key=True)

    def __str__(self):
        return f'User: chat_id = {self.user_id}'
    

class Words(Base):
    __tablename__ = 'words'

    word_id = sq.Column(sq.Integer, primary_key=True)
    original_word = sq.Column(sq.String(length=60)) 
    translate_word = sq.Column(sq.String(length=60))

    def __str__(self):
        return f'Word {self.word_id} has name {self.original_word} and translate {self.translate_word}'
    

class UserWords(Base):
    __tablename__ = 'users_words'

    id = sq.Column(sq.Integer, primary_key=True)
    word_id = sq.Column(sq.Integer,  sq.ForeignKey('words.id'), nullable=False)
    user_id = sq.Column(sq.Integer,  sq.ForeignKey('users.id'), nullable=True)


    def __str__(self):
        return f'{id}: User with {self.user_id} has word {self.word_id}'
