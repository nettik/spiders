import time
from urllib import parse
from selenium import webdriver
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from tqdm import tqdm
from bs4 import BeautifulSoup
from version1.classes.CityAirInfo import CityAirInfo
from version1.classes.CityInfo import CityInfo

# 参考
# https://www.pythonf.cn/read/160255

connectStr = "mysql+pymysql://root:root@localhost:3306/airinfodb"
engine = create_engine(connectStr, max_overflow=5)
Session = sessionmaker(bind=engine)

base_url = 'https://www.aqistudy.cn/historydata/daydata.php?city={}&month={}'


def get_city_list():
    session = Session()
    city_list = session.query(CityInfo).all()
    return [city.cityName for city in city_list]


def get_month_list(start_date="201312", end_date="202012"):
    month_list = list()
    date = start_date[:]
    dt = datetime.strptime(start_date, "%Y%m")
    while date <= end_date:
        month_list.append(date)
        dt = dt + timedelta(weeks=3)
        date = datetime.strftime(dt, "%Y%m")
    return sorted(list(set(month_list)))


def get_parse_html(driver, city, month):
    air_info = list()
    url = base_url.format(parse.quote(city), month)
    driver.get(url)
    time.sleep(1)
    html = driver.page_source
    time.sleep(1)
    soup = BeautifulSoup(html, "html5lib")
    lines = soup.find_all("tr")
    if len(lines) == 1:
        return air_info
    for index in range(len(lines) - 1):
        tds = lines[index + 1].find_all("td")
        air_info.append(CityAirInfo(
            city,
            tds[0].text, tds[1].text, tds[2].text, tds[3].text,
            tds[4].text, tds[5].text, tds[6].text, tds[7].text, tds[8].text
        ))
    return air_info


def main():
    driver = webdriver.PhantomJS()
    session = Session()
    city_list = get_city_list()
    month_list = get_month_list()
    for city in tqdm(city_list):
        city_air_info = list()
        for month in month_list:
            data = get_parse_html(driver, city, month)
            city_air_info.extend(data)
        try:
            session.add_all(city_air_info)
            session.commit()
        except Exception:
            session.rollback()
    driver.close()
    session.close()


# 使用PhantomJS进行数据抓取
if __name__ == '__main__':
    main()
