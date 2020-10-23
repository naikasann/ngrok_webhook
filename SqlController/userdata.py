#model class
from sqlalchemy import Column,Integer,String,Text
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from SqlController.database import init_db

Base=declarative_base()

class UserData(Base):
    # sql database table name.
    __tablename__="usertable"
    # Declaration of each column in the userdata table
    id=Column(String,primary_key=True)
    device_id=Column(String(255))
    password=Column(String(255))

    def __init__(self,id=None,device_id=None,password=None):
        """
        function : Initialize the class.
                　　It also declares the variables in the class.
        """
        self.id=id
        self.device_id=device_id
        self.password=password
        # database class cast.
        init_db()

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

    def getByList(self, arr):
        """
        function :　Converts the specified list to a dictionary list and returns it.
        return   :  table variable.(list<dict>)
        """
        res=[]
        for item in arr:
            res.append(item.toDict())
        return res

    def createConnection():
        # create session.
        engine=create_engine("sqlite:///database.sqlite3")
        Session=sessionmaker(bind=engine)
        ses=Session()

        return ses

    #get all userdata record
    def getAll():
        """
        function :　Retrieve all columns of the user table
        return   :  All data in the usertable. (maybe : list?)
        """
        # create session.
        ses=UserData.createConnection()
        # Get all of the Userdata
        res=ses.query(UserData).all()
        # session close.
        ses.close()

        return res

    def makeRegistration(id, deviceid, password):
        error_list = []
        # create session.
        ses=UserData.createConnection()
        # Creates an instance of user data for registration
        userdata=UserData(id=id,device_id=deviceid,password=password)

        # TODO : It should be filtered with regular expressions for registration.
        # now  : It's all registered.

        # Make sure there are no duplicate ID.
        if(len(ses.query(UserData).filter(UserData.id==id).all())>=1):
            doregister=False
            error_list.append("IDが重複しています！")
        # Make sure there are no duplicate DevID.
        if(len(ses.query(UserData).filter(UserData.device_id==deviceid).all())>=1):
            doregister=False
            error_list.append("デバイスIDが重複しています！")
        else:
            doregister=True

        # To register or not to register.
        if doregister:
            # Since there is none, run a database entry
            ses.add(userdata)
            ses.commit()
            ses.close()
            return True, error_list
        else:
            # Returning a list of error messages without registering
            return False, error_list