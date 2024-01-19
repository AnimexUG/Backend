from sqlalchemy import Column, Float, Integer, String, DateTime
from Connections.connections import Base,engine
import datetime

class SensorData(Base):
    __tablename__ = 'sensor_data'

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String)
    lng = Column(Float)
    lat = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.drop_all(engine) 
Base.metadata.create_all(engine)

