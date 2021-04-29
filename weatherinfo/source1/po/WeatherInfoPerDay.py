from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DECIMAL

Base = declarative_base()


class WeatherInfoPerDay(Base):
    __tablename__ = "weather_info_per_day"
    locationId = Column(String(10), primary_key=True)
    date = Column(String(12), primary_key=True)
    sunrise = Column(String(8))
    sunset = Column(String(8))
    moonrise = Column(String(8))
    moonset = Column(String(8))
    moonPhase = Column(String(32))
    tempMax = Column(DECIMAL(8, 1))
    tempMin = Column(DECIMAL(8, 1))
    textDay = Column(String(16))
    textNight = Column(String(16))
    wind360Day = Column(DECIMAL(12, 1))
    windDirDay = Column(String(16))
    windScaleDay = Column(String(16))
    windSpeedDay = Column(DECIMAL(12, 1))
    wind360Night = Column(DECIMAL(12, 1))
    WindDirNight = Column(String(16))
    windScaleNight = Column(String(16))
    windSpeedNight = Column(DECIMAL(12, 1))
    humidity = Column(DECIMAL(12, 1))
    precip = Column(DECIMAL(12, 1))
    pressure = Column(DECIMAL(12, 1))
    vis = Column(DECIMAL(12, 1))
    cloud = Column(DECIMAL(12, 1))
    uvIndex = Column(DECIMAL(12, 1))

    def __init__(self, locationId, date, sunrise, sunset, moonrise, moonset,
                 moonPhase, tempMax, tempMin, textDay, textNight, wind360Day,
                 windDirDay, windScaleDay, windSpeedDay, wind360Night, WindDirNight, windScaleNight, windSpeedNight,
                 humidity, precip, pressure, vis, cloud, uvIndex):
        self.locationId = locationId
        self.date = date
        self.sunrise = sunrise
        self.sunset = sunset
        self.moonrise = moonrise
        self.moonset = moonset
        self.moonPhase = moonPhase
        self.tempMax = tempMax
        self.tempMin = tempMin
        self.textDay = textDay
        self.textNight = textNight
        self.wind360Day = wind360Day
        self.windDirDay = windDirDay
        self.windScaleDay = windScaleDay
        self.windSpeedDay = windSpeedDay
        self.wind360Night = wind360Night
        self.WindDirNight = WindDirNight
        self.windScaleNight = windScaleNight
        self.windSpeedNight = windSpeedNight
        self.humidity = humidity
        self.precip = precip
        self.pressure = pressure
        self.vis = vis
        self.cloud = cloud
        self.uvIndex = uvIndex