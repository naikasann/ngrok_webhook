from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine=create_engine("sqlite:///sigfoxdatabase.db")
db_session=scoped_session(sessionmaker(bind=engine))
Base=declarative_base()

def init_db():
    # import Database.users
    Base.metadata.create_all(bind=engine)