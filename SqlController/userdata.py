#model class
from sqlalchemy import Column,Integer,String,Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

from SqlController.MysqlController import MysqlController

class UserData(Base):
    # sql database table name.
    __tablename__="userdata"

    # Declaration of each column in the userdata table 
    id=Column(String,primary_key=True)
    device_id=Column(String(255))
    password=Column(String(255))
    # database class cast.
    sqlcontroller = MysqlController()

    def __init__(self,id=None,device_id=None,password=None):
        """
        function : Initialize the class.
                　　It also declares the variables in the class.
        """
        self.id=id
        self.device_id=device_id
        self.password=password

    def toDict(self):
        """
        function :　Each value of the table is returned as a dictionary type.
                    (WARNING : Since we return a variable in the class,
                    we move the function to be retrieved before that.)
        return   :  table variable.
        """
        return{
            "id":str(self.id),
            "device_id":str(self.device_id),
            "password":str(self.password)
        }

    def getByList(arr):
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
        res=ses.query(UserData).all()
        ses.close()
        return res
