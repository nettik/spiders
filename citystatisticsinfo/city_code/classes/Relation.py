from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class Relation(Base):
    __tablename__ = "relation"
    province_code = Column(String(16), primary_key=True)
    province_name = Column(String(16))
    city_code = Column(String(16), primary_key=True)
    city_name = Column(String(32))
    county_code = Column(String(16), primary_key=True)
    county_name = Column(String(64))
    street_code = Column(String(16), primary_key=True)
    street_name = Column(String(64))
    neighborhood_code = Column(String(16), primary_key=True)
    neighborhood_name = Column(String(64))

    def __init__(self, province_code, city_code, county_code, street_code, neighborhood_code,
                 province_name, city_name, county_name, street_name, neighborhood_name):
        self.province_code = province_code
        self.city_code = city_code
        self.county_code = county_code
        self.street_code = street_code
        self.neighborhood_code = neighborhood_code
        self.province_name = province_name
        self.city_name = city_name
        self.county_name = county_name
        self.street_name = street_name
        self.neighborhood_name = neighborhood_name

    def to_list(self):
        return [self.province_code, self.province_name,
                self.city_code, self.city_name,
                self.county_code, self.county_name,
                self.street_code, self.street_name,
                self.neighborhood_code, self.neighborhood_name]
