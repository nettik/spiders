from city_code.crawl import crawl_province, crawl_city, crawl_county, crawl_street, crawl_neighborhood
import time
from functools import wraps
from city_code.classes.Relation import Relation
from city_code.classes.NameCode import NameCode
from tqdm import tqdm
import pandas

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import traceback

connectStr = "mysql+pymysql://root:root@localhost:3306/citystatisticsinfodb"
engine = create_engine(connectStr, max_overflow=5)
Session = sessionmaker(bind=engine)
db_session = Session()


def timer(func):
    @wraps(func)
    def wrapper():
        start = time.time()
        func()
        print("运行时间:" + str(round((time.time() - start) / 60, 1)) + "分钟")

    return wrapper


def make_relation(province, city, county, street, neighborhood_list):
    result = list()
    for neighborhood in neighborhood_list:
        relation = Relation(
            province["code"],
            city["code"],
            county["code"],
            street["code"],
            neighborhood["code"],
            province["name"],
            city["name"],
            county["name"],
            street["name"],
            neighborhood["name"],
        )
        result.append(relation)
        try:
            db_session.add_all(result)
            db_session.commit()
        except:
            db_session.rollback()
            traceback.print_exc()


def save_name_code(area_list, genre):
    if area_list is None:
        return
    result = list()
    for item in area_list:
        namecode = NameCode(item["name"], item["code"], genre)
        result.append(namecode)
    try:
        db_session.add_all(result)
        db_session.commit()
    except:
        db_session.rollback()
        traceback.print_exc()


header_list = ["省代码", "省名称", "市代码", "市名称", "区/县代码", "区/县名称",
               "镇/乡/街道代码", "镇/乡/街道名称", "村委会/居委会代码", "村委会/居委会名称"]
file_path = "D:\\6-baiduyun\\2-数据\\6-城市统计数据\\2-城市代码\\{}.xls"


def save_in_file(province_name):
    db_data = db_session.query(Relation).filter(Relation.province_name == province_name).all()
    df = pandas.DataFrame([item.to_list() for item in db_data])
    df.to_excel(file_path.format(province_name), index=False, header=header_list)


@timer
def main():
    sleep_time = 3
    province_list = crawl_province()[2:3]
    if province_list is not None:
        save_name_code(province_list, "1")
        for province in tqdm(province_list, desc="省"):
            city_list = crawl_city(province["province_link"])
            time.sleep(sleep_time)
            if city_list is not None:
                save_name_code(city_list, "2")
                for city in tqdm(city_list, desc="市"):
                    county_list = crawl_county(city["city_link"])
                    time.sleep(sleep_time)
                    if county_list is not None:
                        save_name_code(county_list, "3")
                        for county in tqdm(county_list, desc="区"):
                            street_list = crawl_street(province["code"] + "/", county["county_link"])
                            time.sleep(sleep_time)
                            if street_list is not None:
                                save_name_code(street_list, "4")
                                for street in tqdm(street_list, desc="街道"):
                                    neighborhood_list = crawl_neighborhood(province["code"] + "/",
                                                                           county["county_link"],
                                                                           street["street_link"])
                                    time.sleep(sleep_time)
                                    save_name_code(neighborhood_list, "5")
                                    make_relation(province, city, county, street, neighborhood_list)
            save_in_file(province["name"])


if __name__ == '__main__':
    engine.execute("delete from name_and_code")
    engine.execute("delete from relation")
    main()