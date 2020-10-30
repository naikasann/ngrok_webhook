#model class
from sqlalchemy import Column,Integer,String,Text
from sqlalchemy.schema import ForeignKey
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.sqltypes import INTEGER

from Database.database import init_db
from Database.postdatas import PostDatas

Base=declarative_base()

class GpsDatas(Base):
    # sql database table name.
    __tablename__="gps_datas"
    # Declaration of each column in the userdata table
    data_id=Column(INTEGER, ForeignKey(PostDatas.data_id), primary_key=True, nullable=False, unique=True)
    lat=Column(INTEGER, nullable=False)
    lng=Column(INTEGER, nullable=False)
    radius=Column(INTEGER, nullable=False)

    def __init__(self, data_id=None, lat=None, lng=None, radius=None):
        """
        function : Initialize the class.
                　　It also declares the variables in the class.
        """
        self.data_id=data_id
        self.lat=lat
        self.lng=lng
        self.radius=radius
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
        ses=GpsDatas.createConnection()
        # Get all of the Userdata
        res=ses.query(GpsDatas).all()
        # session close.
        ses.close()

        return res

    def doRecord(lat, lng, radius, data_id=None):
        # create session.
        ses=GpsDatas.createConnection()
        # record data.
        record_data=GpsDatas(data_id=data_id, lat=lat, lng=lng, radius=radius)

        # TODO : If you need to check for errors when recording data, I'll include it.
        ses.add(record_data)
        ses.commit()
        ses.close()

    def getData(data_id):
        # create session.
        ses=GpsDatas.createConnection()
        # Extract all of them by specifying the data ID.
        datalist = ses.query(GpsDatas).filter(GpsDatas.data_id==data_id).all()

        return datalist