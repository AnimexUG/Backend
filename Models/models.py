from sqlalchemy import Column, Float, Integer, DateTime
from Connections.connections import Base,engine
import datetime

class SensorData(Base):
    __tablename__ = 'sensor_data'

    id = Column(Integer, primary_key=True, index=True)
    lng = Column(Float)
    lat = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(engine)