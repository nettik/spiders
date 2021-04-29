from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from source1.po.CityInfo import CityInfo
from tqdm import tqdm
from source1.GetWeatherInfo import GetWeatherInfo
import time
from datetime import datetime
from datetime import timedelta

key = "b2c9df18452243c3b960452b9d03de2d"
file_path = "D:\\6-baiduyun\\2-数据\\2-气象预报\\{}.xls"
weather_url = "https://devapi.qweather.com/v7/weather/3d?"


def get_locationIds():
    connectStr = "mysql+pymysql://root:root@localhost:3306/weatherinfodb"
    engine = create_engine(connectStr, max_overflow=5)
    engine.execute("delete from weather_info_per_day")
    Session = sessionmaker(bind=engine)
    session = Session()
    result = []
    for obj in session.query(CityInfo.locationId).filter(CityInfo.locationName == CityInfo.adm2):
        result.append(obj[0])
    session.close()
    return result


def main():
    id_list = get_locationIds()
    obj_weather_info = GetWeatherInfo(key, weather_url)
    for location_id in tqdm(id_list):
        obj_weather_info.get_weather_info(location_id)
        time.sleep(0.4)
    forcast_days = int(weather_url.split("/")[-1][0:-2])
    date_list = [(datetime.now() + timedelta(days=index)).strftime("%Y-%m-%d") for index in range(0, forcast_days)]
    for date in date_list:
        obj_weather_info.save_in_file(date, file_path)


if __name__ == '__main__':
    main()
