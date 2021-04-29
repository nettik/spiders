from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DECIMAL

Base = declarative_base()


class FundInfo(Base):
    __tablename__ = "fund_info_new"

    jjbh = Column(String(12), primary_key=True)
    jjmc = Column(String(64))
    jjlx = Column(String(16))
    jjbq = Column(String(255))
    clsj = Column(String(12))
    jjgm = Column(String(32))
    jnsyl = Column(DECIMAL(8, 2))
    yzsyl = Column(DECIMAL(8, 2))
    yysyl = Column(DECIMAL(8, 2))
    sysyl = Column(DECIMAL(8, 2))
    lysyl = Column(DECIMAL(8, 2))
    ynsyl = Column(DECIMAL(8, 2))
    lnsyl = Column(DECIMAL(8, 2))
    snsyl = Column(DECIMAL(8, 2))
    ynxpl = Column(DECIMAL(8, 2))
    lnxpl = Column(DECIMAL(8, 2))
    snxpl = Column(DECIMAL(8, 2))
    cgczbl = Column(String(600))
    zcpz = Column(String(300))
    hypz = Column(String(300))

    def to_list(self):
        return [self.jjbh, self.jjmc, self.jjlx,
                self.jjbq, self.clsj, self.jjgm,
                self.jnsyl, self.yzsyl, self.yysyl,
                self.sysyl, self.lysyl, self.ynsyl,
                self.lnsyl, self.snsyl, self.ynxpl,
                self.lnxpl, self.snxpl, self.cgczbl, self.zcpz, self.hypz]

    def __init__(self, jjbh="", jjmc="", jjlx="", jjbq="", clsj="", jjgm="", jnsyl=0,
                 yzsyl=0, yysyl=0, sysyl=0, lysyl=0, ynsyl=0, lnsyl=0, snsyl=0,
                 ynxpl=0, lnxpl=0, snxpl=0, cgczbl="", zcpz="", hypz=""):
        self.jjbh = jjbh
        self.jjmc = jjmc
        self.jjlx = jjlx
        self.jjbq = jjbq
        self.clsj = clsj
        self.jjgm = jjgm
        self.jnsyl = jnsyl
        self.yzsyl = yzsyl
        self.yysyl = yysyl
        self.sysyl = sysyl
        self.lysyl = lysyl
        self.ynsyl = ynsyl
        self.lnsyl = lnsyl
        self.snsyl = snsyl
        self.ynxpl = ynxpl
        self.lnxpl = lnxpl
        self.snxpl = snxpl
        self.cgczbl = cgczbl
        self.zcpz = zcpz
        self.hypz = hypz
