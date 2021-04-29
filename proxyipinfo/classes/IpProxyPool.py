from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class IpProxyPool(Base):
    __tablename__ = "ip_proxy_pool"
    ip = Column(String(15), primary_key=True)
    port = Column(Integer, primary_key=True)
    anonymous = Column(String(16))
    proxyType = Column(String(16))
    location = Column(String(64))

    def __init__(self, ip, port, anonymous, proxyType, location):
        self.ip = ip
        self.port = port
        self.anonymous = anonymous
        self.proxyType = proxyType
        self.location = location
