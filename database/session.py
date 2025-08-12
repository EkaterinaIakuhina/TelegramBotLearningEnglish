import sqlalchemy as sq
from models import Base
from sqlalchemy.orm import sessionmaker
import dotenv
import os


dotenv.load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_HOST=os.getenv('DB_HOST')
DB_PORT=os.getenv('DB_PORT')
DB_USER=os.getenv('DB_USER')
DB_PASSWORD=os.getenv('DB_PASSWORD')



DSN = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = sq.create_engine(
    url=DSN,
    echo=True,



    )

Session = sessionmaker(bind=engine)


def create_db():
    Base.metadata.create_all(engine)

def get_session():
   pass