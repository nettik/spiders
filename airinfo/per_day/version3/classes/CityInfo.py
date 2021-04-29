from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()


class CityInfo(Base):
    __tablename__ = "city_info"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cityName = Column(String(32))

    def __init__(self, cityName):
        self.cityName = cityName
