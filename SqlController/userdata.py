#model class
from sqlalchemy import Column,Integer,String,Text
from SqlController.database import Base

from SqlController.database import init_db

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
class UserData(Base):
    __tablename__="userdata"

    id=Column(String,primary_key=True)
    device_id=Column(String(255))
    password=Column(String(255))
    init_db()
    def __init__(self,id=None,device_id=None,password=None):
        self.id=id
        self.device_id=device_id
        self.password=password

   #get Dict data
    def toDict(self):
        return{
            "id":str(self.id),
            "device_id":str(self.device_id),
            "password":str(self.password)
        }
    
    #get List data
    def getByList(arr):
        res=[]
        for item in arr:
            res.append(item.toDict())
        return res
    
    #get all userdata record
    def getAll():
        engine=create_engine("sqlite:///user.sqlite3")
        Session=sessionmaker(bind=engine)
        ses=Session()
        res=ses.query(UserData).all()
        ses.close()
        return res
