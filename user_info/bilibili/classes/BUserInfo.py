from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()


class BUserInfo(Base):
    __tablename__ = "bilibili_user"
    userid = Column(String(12), primary_key=True)
    name = Column(String(32))
    gender = Column(String(4))
    birthday = Column(String(6))
    level = Column(String(2))
    sign = Column(String(256))
    fans = Column(Integer())
    follows = Column(Integer())
    likes = Column(Integer())
    articles = Column(Integer())
    archives = Column(Integer())
    tags = Column(String(64))

    def set_userid(self, userid):
        self.userid = userid

    def set_name(self, name):
        self.name = name

    def set_gender(self, gender):
        self.gender = gender

    def set_birthday(self, birthday):
        self.birthday = birthday

    def set_level(self, level):
        self.level = level

    def set_sign(self, sign):
        self.sign = sign

    def set_fans(self, fans):
        self.fans = fans

    def set_follows(self, follows):
        self.follows = follows

    def set_likes(self, likes):
        self.likes = likes

    def set_articles(self, articles):
        self.articles = articles

    def set_archives(self, archives):
        self.archives = archives

    def set_tags(self, tags):
        self.tags = tags

    def __init__(self):
        self.userid = ""
        self.name = ""
        self.gender = ""
        self.birthday = ""
        self.level = ""
        self.sign = ""
        self.fans = 0
        self.follows = 0
        self.likes = 0
        self.articles = 0
        self.archives = 0
        self.tags = ""
