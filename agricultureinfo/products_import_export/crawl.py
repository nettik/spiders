from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm
from products_import_export.import_fun import parse_import, crawl_import
from products_import_export.export_fun import parse_export, crawl_export

from products_import_export.classes.ProductsIE import ProductsIE

# http://zdscxx.moa.gov.cn:8080/nyb/pc/index.jsp

connectStr = "mysql+pymysql://root:root@localhost:3306/agricultureinfo"
engine = create_engine(connectStr, max_overflow=5)
Session = sessionmaker(bind=engine)


def agriculture_import(year_list, month_list):
    session = Session()
    for year in tqdm(year_list):
        for month in month_list:
            raw_data = crawl_import(year, month)
            if raw_data != "":
                foreign_data, china_data = parse_import(raw_data)
                if foreign_data is not None and china_data is not None:
                    # 中国
                    product_c = ProductsIE("中国", year, month)
                    product_c.import_num = china_data
                    try:
                        session.add(product_c)
                        session.commit()
                    except Exception as e:
                        print(e)
                        session.rollback()
                    # 外国
                    for item in foreign_data:
                        if item["name"] == "中国（大陆）":
                            continue
                        product = ProductsIE(item["name"], year, month)
                        product.import_num = item["value"]
                        try:
                            session.add(product)
                            session.commit()
                        except Exception as e:
                            print(e)
                            session.rollback()


def agriculture_export(year_list, month_list):
    session = Session()
    for year in tqdm(year_list):
        for month in month_list:
            raw_data = crawl_export(year, month)
            if raw_data != "":
                foreign_data, china_data = parse_export(raw_data)
                if foreign_data is not None and china_data is not None:
                    # 中国
                    try:
                        session.query(ProductsIE).filter(
                            and_(ProductsIE.country == "中国", ProductsIE.year == year,
                                 ProductsIE.month == month)).update({"export_num": china_data})
                        session.commit()
                    except Exception as e:
                        print(e)
                        session.rollback()
                    # 外国
                    for item in foreign_data:
                        if item["name"] == "中国（大陆）":
                            continue
                        try:
                            session.query(ProductsIE).filter(
                                and_(ProductsIE.country == item["name"], ProductsIE.year == year,
                                     ProductsIE.month == month)).update({"export_num": item["value"]})
                            session.commit()
                        except Exception as e:
                            print(e)
                            session.rollback()


def main():
    year = ["2017", "2018", "2019", "2020", "2021"]
    month = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    # agriculture_import(year, month)
    agriculture_export(year, month)


if __name__ == '__main__':
    main()
