from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class MoiveInfo(Base):
    __tablename__ = "moive_info"
    name = Column(String(128), primary_key=True)
    region = Column(String(128), primary_key=True)
    director = Column(String(128))
    editor = Column(String(128))
    leading_role = Column(String(128))
    moive_type = Column(String(128))
    language = Column(String(128))
    date = Column(String(10))
    duration = Column(String(12))
    box_office = Column(String(128))

    def set_name(self, name):
        self.name = name.replace("<span>", "").replace("</span>", "").replace("\n", "").replace(" ", "")

    def set_director(self, director):
        self.director = director.replace("\n", "").replace(" ", "")

    def set_editor(self, editor):
        temp = [item.replace("\n", "").replace(" ", "") for item in editor]
        self.editor = ",".join(temp)

    def set_leading_role(self, leading_role):
        temp = [item.replace("\n", "").replace(" ", "") for item in leading_role]
        self.leading_role = ",".join(temp)

    def set_moive_type(self, moive_type):
        self.moive_type = moive_type.replace("\n", "").replace(" ", "")

    def set_region(self, region):
        self.region = region.replace("\n", "").replace(" ", "")

    def set_language(self, language):
        self.language = language.replace("\n", "").replace(" ", "")

    def set_date(self, date):
        self.date = date

    def set_duraton(self, duration):
        self.duration = duration.replace("\n", "").replace(" ", "")

    def set_box_office(self, box_office):
        self.box_office = box_office

    def __init__(self):
        self.name = ""
        self.region = ""
        self.director = ""
        self.editor = ""
        self.leading_role = ""
        self.moive_type = ""
        self.language = ""
        self.date = ""
        self.duration = ""
        self.box_office = ""

    def to_list(self):
        return [self.name, self.region, self.director, self.editor, self.leading_role, self.moive_type, self.language,
                self.date, self.duration, self.box_office]
