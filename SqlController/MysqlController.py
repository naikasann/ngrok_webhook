from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class MysqlController:
    def __init__(self):
        # Database initialize.
        engine=create_engine("sqlite:///user.sqlite3")
        db_session=scoped_session(sessionmaker(bind=engine))
        Base=declarative_base()
        Base.metadata.create_all(bind=engine)