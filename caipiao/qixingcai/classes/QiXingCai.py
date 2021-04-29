from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class QiXingCai(Base):
    __tablename__ = "qi_xing_cai"
    index = Column(String(8), primary_key=True)
    date = Column(String(32))
    orange1 = Column(String(2))
    orange2 = Column(String(2))
    orange3 = Column(String(2))
    orange4 = Column(String(2))
    orange5 = Column(String(2))
    orange6 = Column(String(2))
    orange7 = Column(String(2))
    sale_money = Column(String(16))
    pool_money = Column(String(16))
    first_prize_num = Column(String(16))
    first_prize_money = Column(String(16))
    second_prize_num = Column(String(16))
    second_prize_money = Column(String(16))
    third_prize_num = Column(String(16))
    third_prize_money = Column(String(16))

    def __init__(self, index):
        self.index = index
        self.date = ""
        self.orange1 = ""
        self.orange2 = ""
        self.orange3 = ""
        self.orange4 = ""
        self.orange5 = ""
        self.orange6 = ""
        self.orange7 = ""
        self.sale_money = 0
        self.pool_money = 0
        self.first_prize_num = ""
        self.first_prize_money = ""
        self.second_prize_num = ""
        self.second_prize_money = ""
        self.third_prize_num = ""
        self.third_prize_money = ""

    def to_list(self):
        return [self.index, self.date, self.orange1, self.orange2, self.orange3, self.orange4, self.orange5,
                self.orange6, self.orange7,
                self.sale_money,
                self.pool_money, self.first_prize_num, self.first_prize_money, self.second_prize_num,
                self.second_prize_money,
                self.third_prize_num, self.third_prize_money]
