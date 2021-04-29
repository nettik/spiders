from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class NameCode(Base):
    __tablename__ = "name_and_code"
    name = Column(String(128), primary_key=True)
    code = Column(String(16), primary_key=True)
    genre = Column(String(1))

    def __init__(self, name, code, genre):
        self.name = name
        self.code = code
        self.genre = genre
