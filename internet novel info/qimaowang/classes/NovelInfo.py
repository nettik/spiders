from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TEXT

Base = declarative_base()


class NovelInfo(Base):
    __tablename__ = "qimao_novel_info"

    # 书名
    book_name = Column(String(32), primary_key=True)
    # 作者
    author = Column(String(16), primary_key=True)
    # 评分
    rank = Column(String(12))
    # 状态-连载、完结
    state = Column(String(16))
    # 类型
    book_type = Column(String(80))
    # 主角
    leading_role = Column(String(64))
    # 字数
    scale = Column(String(20))
    # 阅读数量
    reading_num = Column(String(32))
    # 人气值
    popularity = Column(String(32))
    # 简介
    introduction = Column(TEXT())

    def __init__(self, book_name, author):
        self.book_name = book_name
        self.author = author
        # 评分
        self.rank = ""
        # 状态-连载、完结
        self.state = ""
        # 类型
        self.book_type = ""
        # 主角
        self.leading_role = ""
        # 字数
        self.scale = ""
        # 阅读数量
        self.reading_num = ""
        # 人气值
        self.popularity = ""
        # 简介
        self.introduction = ""
