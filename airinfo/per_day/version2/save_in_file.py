import pandas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

from version2.classes.CityAirInfo import CityAirInfo
from version2.classes.CityInfo import CityInfo

connectStr = "mysql+pymysql://root:root@localhost:3306/airinfodb"
engine = create_engine(connectStr, max_overflow=5)
Session = sessionmaker(bind=engine)

path = "D:\\6-baiduyun\\2-数据\\3-空气质量\\{}.xls"

header_list = ["日期", "aqi", "质量等级", "PM2.5", "PM10", "SO2", "CO", "NO2", "O3"]


def get_city_list():
    session = Session()
    city_list = session.query(CityInfo).all()
    return [city.cityName for city in city_list]


def main():
    session = Session()
    city_list = get_city_list()
    for city in tqdm(city_list):
        data = session.query(CityAirInfo).filter(CityAirInfo.cityName == city).all()
        if len(data) == 0:
            continue
        data_list = [info.to_list() for info in data]
        df = pandas.DataFrame(data_list)
        df.to_excel(path.format(city), header=header_list, index=False)


if __name__ == '__main__':
    main()
