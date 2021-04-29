from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class QiLeCai(Base):
    __tablename__ = "qi_le_cai"
    index = Column(String(8), primary_key=True)
    date = Column(String(32))
    red1 = Column(String(2))
    red2 = Column(String(2))
    red3 = Column(String(2))
    red4 = Column(String(2))
    red5 = Column(String(2))
    red6 = Column(String(2))
    red7 = Column(String(2))
    blue = Column(String(2))
    sale_money = Column(String(16))
    first_prize_num = Column(String(16))
    first_prize_money = Column(String(16))
    second_prize_num = Column(String(16))
    second_prize_money = Column(String(16))
    third_prize_num = Column(String(16))
    third_prize_money = Column(String(16))

    def __init__(self, index):
        self.index = index
        self.date = ""
        self.red1 = ""
        self.red2 = ""
        self.red3 = ""
        self.red4 = ""
        self.red5 = ""
        self.red6 = ""
        self.red7 = ""
        self.blue = ""
        self.sale_money = 0
        self.first_prize_num = ""
        self.first_prize_money = ""
        self.second_prize_num = ""
        self.second_prize_money = ""
        self.third_prize_num = ""
        self.third_prize_money = ""

    def to_list(self):
        return [self.index, self.date, self.red1, self.red2, self.red3, self.red4, self.red5,
                self.red6, self.red7, self.blue, self.sale_money, self.first_prize_num,
                self.first_prize_money, self.second_prize_num,
                self.second_prize_money,
                self.third_prize_num, self.third_prize_money]
