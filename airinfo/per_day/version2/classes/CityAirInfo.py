from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CityAirInfo(Base):
    __tablename__ = "city_air_info"

    cityName = Column(String(32), primary_key=True)
    date = Column(String(12), primary_key=True)
    aqi = Column(Integer())
    quality = Column(String(12))
    PM2_5 = Column(Integer())
    PM10 = Column(Integer())
    so2 = Column(Integer())
    co = Column(Integer())
    no2 = Column(Integer())
    o3_8h = Column(Integer())

    def __init__(self, cityName, date, aqi, quality, PM2_5, PM10, so2, co, no2, o3_8h):
        self.cityName = cityName
        self.date = date
        self.aqi = aqi
        self.quality = quality
        self.PM2_5 = PM2_5
        self.PM10 = PM10
        self.so2 = so2
        self.co = co
        self.no2 = no2
        self.o3_8h = o3_8h

    def to_list(self):
        return [self.date, self.aqi, self.quality, self.PM2_5, self.PM10, self.so2, self.co, self.no2,
                self.o3_8h]
