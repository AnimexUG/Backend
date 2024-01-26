from sqlalchemy import Column, Float, Integer, String, DateTime
from Connections.connections import Base,engine
import datetime
from hashing import Harsher
from pydantic import BaseModel


class SensorData(Base):
    __tablename__ = 'sensor_data'

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String)
    lng = Column(Float)
    lat = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def get_data_by_device_id(db_session, device_id):
        return db_session.query(SensorData).filter(SensorData.device_id == device_id).all()
    
    @staticmethod
    def get_unique_devices(db_session):
        return db_session.query(SensorData.device_id).distinct().all()
# Base.metadata.drop_all(engine) 

class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True, index=True) 
    username = Column(String)
    password = Column(String)
    email = Column(String)

    @staticmethod
    def get_admin(db_session):
        return db_session.query(Admin).all()
    
    @staticmethod
    def username_exists(db_session, username):
        return db_session.query(Admin).filter(Admin.username == username).first() is not None
    
    @staticmethod
    def get_username(db_session):
        return db_session.query(Admin.username).all()
    
    @staticmethod
    def get_userdata_by_username(db_session, username):
        return db_session.query(Admin).filter(Admin.username == username).first()

    @staticmethod
    def confirm_password_login(db_session, username, password):
       # username can be username or email
        return db_session.query(Admin).filter(Admin.username == username, Admin.password == password).first()
    
    def update_password(self, new_password):
        hashed_password = Harsher.get_hash_password(new_password)
        print(f"Updating password to: {hashed_password}") 
        self.password = hashed_password

    def update_username(self, new_username_prefix):
        self.username = f"{new_username_prefix}@Animex.ug"

class UsernameChangeRequest(BaseModel):
    current_username: str
    new_username_prefix: str


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

