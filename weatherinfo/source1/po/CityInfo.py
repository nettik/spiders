from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DECIMAL

Base = declarative_base()


class CityInfo(Base):
    __tablename__ = 'city_info'
    locationId = Column(String(10), primary_key=True)
    locationNameEn = Column(String(64))
    locationName = Column(String(128))
    countryCode = Column(String(32))
    countryNameEn = Column(String(128))
    countryName = Column(String(128))
    adm1En = Column(String(128))
    adm1 = Column(String(128))
    adm2En = Column(String(128))
    adm2 = Column(String(128))
    latitude = Column(DECIMAL(16, 8))
    longitude = Column(DECIMAL(16, 8))

    def __init__(self, locationId, locationNameEn, locationName,
                 countryCode, countryNameEn, countryName, adm1En, adm1,
                 adm2En, adm2, latitude, longitude):
        self.locationId = locationId
        self.locationNameEn = locationNameEn
        self.locationName = locationName
        self.countryCode = countryCode
        self.countryNameEn = countryNameEn
        self.countryName = countryName
        self.adm1En = adm1En
        self.adm1 = adm1
        self.adm2En = adm2En
        self.adm2 = adm2
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return "{}:{}".format(self.locationId, self.locationName)
