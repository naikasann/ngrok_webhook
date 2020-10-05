#model class
from sqlalchemy import Column,Integer,String,Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from SqlController.database import init_db

Base=declarative_base()

class ReceiveData(Base):
    # sql database table name.
    __tablename__="receivetable"
    # Declaration of each column in the userdata table
    device_id=Column(String,primary_key=True)
    data=Column(String(255))
    timestamp=Column(String(255))
    rawdata=Column(String(800))

    def __init__(self,device_id=None,data=None,timestamp=None,rawdata=None):
        """
        function : Initialize the class.
                　　It also declares the variables in the class.
        """
        self.device_id=device_id
        self.data=data
        self.timestamp=timestamp
        self.rawdata=rawdata
        # database class cast.
        init_db()
        """engine=create_engine("sqlite:///user.sqlite3")
        db_session=scoped_session(sessionmaker(bind=engine))
        Base=declarative_base()
        Base.metadata.create_all(bind=engine)"""

    def toDict(self):
        """
        function :　Each value of the table is returned as a dictionary type.
                    (WARNING : Since we return a variable in the class,
                    we move the function to be retrieved before that.)
        return   :  table variable.
        """
        return{
            "device_id":str(self.device_id),
            "data":str(self.data),
            "timestamp":str(self.timestamp),
            "rawdata":str(self.rawdata)
        }

    def getByList(self, arr):
        """
        function :　Converts the specified list to a dictionary list and returns it.
        return   :  table variable.(list<dict>)
        """
        res=[]
        for item in arr:
            res.append(item.toDict())
        return res

    #get all userdata record
    def getAll():
        """
        function :　Retrieve all columns of the user table
        return   :  All data in the usertable. (maybe : list?)
        """
        engine=create_engine("sqlite:///user.sqlite3")
        Session=sessionmaker(bind=engine)
        ses=Session()
        res=ses.query(ReceiveData).all()
        ses.close()
        return res