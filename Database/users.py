#model class
from enum import unique
from sqlalchemy import Column,Integer,String,Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from Database.database import init_db

Base=declarative_base()

class Users(Base):
    # sql database table name.
    __tablename__="users"
    # Declaration of each column in the userdata table
    id=Column(Text(20),primary_key=True, nullable=False, unique=True)
    device_id=Column(Text(20), nullable=False, unique=True)
    password=Column(Text(20), nullable=False)

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

    def createConnection():
        # create session.
        engine=create_engine("sqlite:///sigfoxdatabase.db")
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
        ses=Users.createConnection()
        # Get all of the Userdata
        res=ses.query(Users).all()
        # session close.
        ses.close()

        return res

    def doLogin(id, password):
        # create session.
        ses=Users.createConnection()
        # Refers to the ID entered. (Whether it exists or not.)
        # The return value is the column
        database_id_list=ses.query(Users).filter(Users.id==id).all()
        for database_id in database_id_list:
            if str(database_id.password)==str(password):
                # all_data=ses.query(ReceiveData).filter(ReceiveData.device_id==database_id.device_id).all()
                alldata=Users.getAll()
                ses.close()
                return True
        ses.close()
        return False


    def makeRegistration(id, deviceid, password):
        error_list = []
        # create session.
        ses=Users.createConnection()
        # Creates an instance of user data for registration
        regist_data=Users(id=id,device_id=deviceid,password=password)

        # TODO : It should be filtered with regular expressions for registration.
        # now  : It's all registered.

        # Make sure there are no duplicate ID.
        if(len(ses.query(Users).filter(Users.id==id).all())>=1):
            doregister=False
            error_list.append("IDが重複しています！")
        # Make sure there are no duplicate DevID.
        if(len(ses.query(Users).filter(Users.device_id==deviceid).all())>=1):
            doregister=False
            error_list.append("デバイスIDが重複しています！")
        else:
            doregister=True

        # To register or not to register.
        if doregister:
            # Since there is none, run a database entry
            ses.add(regist_data)
            ses.commit()
            ses.close()
            return True, error_list
        else:
            # Returning a list of error messages without registering
            return False, error_list