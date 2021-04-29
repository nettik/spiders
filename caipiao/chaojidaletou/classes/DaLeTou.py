from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class DaLeTou(Base):
    __tablename__ = "da_le_tou"
    index = Column(String(8), primary_key=True)
    date = Column(String(32))
    red1 = Column(String(2))
    red2 = Column(String(2))
    red3 = Column(String(2))
    red4 = Column(String(2))
    red5 = Column(String(2))
    blue1 = Column(String(2))
    blue2 = Column(String(2))
    sale_money = Column(String(16))
    pool_money = Column(String(16))

    def __init__(self, param):
        self.index = param
        self.date = ""
        self.red1 = ""
        self.red2 = ""
        self.red3 = ""
        self.red4 = ""
        self.red5 = ""
        self.blue1 = ""
        self.blue2 = ""
        self.sale_money = ""
        self.pool_money = ""

    def to_list(self):
        return [
            self.index, self.date,
            self.red1, self.red2,
            self.red3, self.red4,
            self.red5, self.blue1,
            self.blue2, self.sale_money, self.pool_money
        ]
