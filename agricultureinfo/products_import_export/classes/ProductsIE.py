from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class ProductsIE(Base):
    __tablename__ = "products_import_export"

    country = Column(String(32), primary_key=True)
    year = Column(String(4), primary_key=True)
    month = Column(String(2), primary_key=True)
    import_num = Column(String(10))
    export_num = Column(String(10))

    def __init__(self, country, year, month):
        self.country = country
        self.year = year
        self.month = month
        self.import_num = ""
        self.export_num = ""

    def to_list(self):
        return [self.country, self.year, self.month, self.import_num, self.export_num]
