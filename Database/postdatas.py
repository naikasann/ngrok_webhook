#model class
from Database.users import Users
from sqlalchemy import Column,Integer,String,Text
from sqlalchemy.orm import create_session, query_expression, sessionmaker
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import INTEGER
from sqlalchemy.schema import ForeignKey

from Database.database import init_db
from Database.users import Users

Base=declarative_base()

class PostDatas(Base):
    # sql database table name.
    __tablename__="post_datas"
    # Declaration of each column in the userdata table
    data_id=Column(INTEGER, primary_key=True, nullable=False, unique=True)
    device_id=Column(Text(20), ForeignKey(Users.device_id), nullable=False)
    recieve_data=Column(String(255), nullable=False)
    timestamp=Column(String(255), nullable=False)

    def __init__(self,data_id=None,device_id=None,recieve_data=None,timestamp=None):
        """
        function : Initialize the class.
                　　It also declares the variables in the class.
        """
        self.data_id=data_id
        self.device_id=device_id
        self.recieve_data=recieve_data
        self.timestamp=timestamp
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
        ses=PostDatas.createConnection()
        # Get all of the Userdata
        res=ses.query(PostDatas).all()
        # session close.
        ses.close()

        return res

    def getDatas(device_id):
        """
        docstring
        """
        pass

    def doRecord(device_id,recieve_data,timestamp, data_id=None):
        # create session.
        ses=PostDatas.createConnection()
        checkses = Users.createConnection()
        # Creates an instance of user data for registration
        userdata=PostDatas(data_id=data_id,device_id=device_id,recieve_data=recieve_data,timestamp=timestamp)
        # TODO : デバイスIDを参照して登録するかどうか決定する。
        if(len(checkses.query(Users).filter(Users.device_id==str(device_id)).all())>=1):
            ses.add(userdata)
            ses.commit()
            ses.close()
            checkses.close()

    """    def getDatasfromDeviceid(device_id):
        # create session.
        ses=PostDatas.createConnection()
        # Extract all of them by specifying the data ID.

        return user_datas"""

    def getLastDataid():
        ses = PostDatas.createConnection()
        query = ses.query(func.max(PostDatas.data_id).label("max_id"))
        last_dataid = query.one()

        return last_dataid