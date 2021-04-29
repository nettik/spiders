from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DECIMAL

Base = declarative_base()


# 草原
class Grass(Base):
    __tablename__ = "grass"
    city = Column(String(32), primary_key=True)
    year2020 = Column(DECIMAL(8, 2))
    year2019 = Column(DECIMAL(8, 2))
    year2018 = Column(DECIMAL(8, 2))
    year2017 = Column(DECIMAL(8, 2))
    year2016 = Column(DECIMAL(8, 2))
    year2015 = Column(DECIMAL(8, 2))
    year2014 = Column(DECIMAL(8, 2))
    year2013 = Column(DECIMAL(8, 2))
    year2012 = Column(DECIMAL(8, 2))
    year2011 = Column(DECIMAL(8, 2))
    year2010 = Column(DECIMAL(8, 2))
    year2009 = Column(DECIMAL(8, 2))
    year2008 = Column(DECIMAL(8, 2))
    year2007 = Column(DECIMAL(8, 2))
    year2006 = Column(DECIMAL(8, 2))
    year2005 = Column(DECIMAL(8, 2))
    year2004 = Column(DECIMAL(8, 2))
    year2003 = Column(DECIMAL(8, 2))
    year2002 = Column(DECIMAL(8, 2))
    year2001 = Column(DECIMAL(8, 2))
    year2000 = Column(DECIMAL(8, 2))

    def __init__(self, city):
        self.city = city
        self.year2020 = 0.0
        self.year2019 = 0.0
        self.year2018 = 0.0
        self.year2017 = 0.0
        self.year2016 = 0.0
        self.year2015 = 0.0
        self.year2014 = 0.0
        self.year2013 = 0.0
        self.year2012 = 0.0
        self.year2011 = 0.0
        self.year2010 = 0.0
        self.year2009 = 0.0
        self.year2008 = 0.0
        self.year2007 = 0.0
        self.year2006 = 0.0
        self.year2005 = 0.0
        self.year2004 = 0.0
        self.year2003 = 0.0
        self.year2002 = 0.0
        self.year2001 = 0.0
        self.year2000 = 0.0

    def set_data(self, year, data):
        if year == "2020":
            self.year2020 = data
        elif year == "2019":
            self.year2019 = data
        elif year == "2018":
            self.year2018 = data
        elif year == "2017":
            self.year2017 = data
        elif year == "2016":
            self.year2016 = data
        elif year == "2015":
            self.year2015 = data
        elif year == "2014":
            self.year2014 = data
        elif year == "2013":
            self.year2013 = data
        elif year == "2012":
            self.year2012 = data
        elif year == "2011":
            self.year2011 = data
        elif year == "2010":
            self.year2010 = data
        elif year == "2009":
            self.year2009 = data
        elif year == "2008":
            self.year2008 = data
        elif year == "2007":
            self.year2007 = data
        elif year == "2006":
            self.year2006 = data
        elif year == "2005":
            self.year2005 = data
        elif year == "2004":
            self.year2004 = data
        elif year == "2003":
            self.year2003 = data
        elif year == "2002":
            self.year2002 = data
        elif year == "2001":
            self.year2001 = data
        elif year == "2000":
            self.year2000 = data

    def to_list(self):
        return [self.city, self.year2020, self.year2019, self.year2018, self.year2017, self.year2016, self.year2015,
                self.year2014, self.year2013, self.year2012, self.year2011, self.year2010, self.year2009,
                self.year2008, self.year2007, self.year2006, self.year2005, self.year2004, self.year2003,
                self.year2002, self.year2001, self.year2000]
