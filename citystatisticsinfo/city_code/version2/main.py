from city_code.common.crawl import crawl_province, crawl_city, crawl_county, crawl_street, crawl_neighborhood
import json
from tqdm import tqdm
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from city_code.common.classes.Relation import Relation
from city_code.common.classes.NameCode import NameCode
import traceback
import pandas

connectStr = "mysql+pymysql://root:root@localhost:3306/citystatisticsinfodb"
engine = create_engine(connectStr, max_overflow=5)
Session = sessionmaker(bind=engine)
db_session = Session()

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


header_list = ["省代码", "省名称", "市代码", "市名称", "区/县代码", "区/县名称",
               "镇/乡/街道代码", "镇/乡/街道名称", "村委会/居委会代码", "村委会/居委会名称"]
file_path = "D:\\6-baiduyun\\2-数据\\6-城市统计数据\\2-城市代码\\{}.xls"


def save_in_file(province_name):
    db_data = db_session.query(Relation).filter(Relation.province_name == province_name).all()
    df = pandas.DataFrame([item.to_list() for item in db_data])
    df.to_excel(file_path.format(province_name), index=False, header=header_list)


def save_province_in_file():
    province_list = crawl_province()
    with open("data/province.json", "w", encoding='utf-8') as f:
        f.write(json.dumps(province_list, ensure_ascii=False))


def save_city_in_file():
    with open("data/province.json", "r", encoding='utf-8') as f:
        data_list = json.loads(f.read())
    for province in tqdm(data_list):
        city_list = crawl_city(province["province_link"])
        province["city"] = city_list
    with open("data/city.json", "w", encoding='utf-8') as f:
        f.write(json.dumps(data_list, ensure_ascii=False))


def save_county_in_file():
    with open("data/city.json", "r", encoding='utf-8') as f:
        data_list = json.loads(f.read())
    for province in tqdm(data_list, desc="省"):
        city_list = province["city"]
        for city in tqdm(city_list, desc="市"):
            county_list = crawl_county(city["city_link"])
            city["county"] = county_list
            time.sleep(1)
    with open("data/county.json", "w", encoding='utf-8') as f:
        f.write(json.dumps(data_list, ensure_ascii=False))


def save_street_in_file():
    # 第一次执行该函数
    # with open("data/county.json", "r", encoding='utf-8') as f:
    #     data_list = json.loads(f.read())
    with open("data/street.json", "r", encoding='utf-8') as f:
        data_list = json.loads(f.read())
    for province in tqdm(data_list[11:12], desc="省"):
        city_list = province["city"]
        for city in tqdm(city_list, desc="市"):
            county_list = city["county"]
            for county in tqdm(county_list, desc="区"):
                if county.get("street") is None:
                    if county["county_link"] != "":
                        street_list = crawl_street(province["code"] + "/", county["county_link"])
                        county["street"] = street_list
                        time.sleep(1)
                    else:
                        county["street"] = None
    with open("data/street.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(data_list, ensure_ascii=False))


def save_data_in_db():
    with open("data/street.json", "r", encoding="utf-8") as f:
        data_list = json.loads(f.read())
    for province in tqdm(data_list, desc="省"):
        city_list = province["city"]
        for city in tqdm(city_list, desc="市"):
            county_list = city["county"]
            for county in tqdm(county_list, desc="区"):
                street_list = county["street"]
                for street in tqdm(street_list, desc="街道"):
                    if county.get("county_link") is not None:
                        neighborhood_list = crawl_neighborhood(province["code"] + "/",
                                                               county["county_link"],
                                                               street["street_link"])
                        time.sleep(1)
                        make_relation(province, city, county, street, neighborhood_list)
        save_in_file(province["name"])

def main():
    save_street_in_file()


if __name__ == '__main__':
    main()
