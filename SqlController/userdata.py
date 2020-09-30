#model class
class UserData(Base):
    __talename__="userdata"

    id=Column(String,primary_key=True)
    device_id=Column(String(255))
    password=Column(String(255))

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
        Session=sessionmaker(bind=engine)
        ses=Session()
        res=ses.query(Mydata).all()
        ses.close()
        return res
