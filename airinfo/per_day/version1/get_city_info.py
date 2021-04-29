import requests
from bs4 import BeautifulSoup
from version1.classes.CityInfo import CityInfo
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from tqdm import tqdm

connectStr = "mysql+pymysql://root:root@localhost:3306/airinfodb"
url = "https://www.aqistudy.cn/historydata/index.php"
cnt = 22


def get_html():
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    response = requests.get(url, headers=header, timeout=1)
    raw_html = response.content.decode("utf-8")
    return raw_html


# body > div:nth-child(4) > div > div.col-lg-9.col-md-8.col-sm-8.col-xs-12 > div.all > div.bottom > ul:nth-child(1)
# body > div:nth-child(4) > div > div.col-lg-9.col-md-8.col-sm-8.col-xs-12 > div.all > div.bottom > ul:nth-child(22)
def get_city_list(html):
    cities = list()
    soup = BeautifulSoup(html, "html5lib")
    css_selector_pattern = "body > div:nth-child(4) > div > div.col-lg-9.col-md-8.col-sm-8.col-xs-12 > div.all > div.bottom > ul:nth-child({})"
    for i in tqdm(range(cnt)):
        selector = css_selector_pattern.format(str(i + 1))
        ul = soup.select(selector)[0]
        li_list = ul.find_all("li")
        cities.extend([CityInfo(li.text.replace(" ", "").strip("\n")) for li in li_list])
    return cities


def main():
    raw_html = get_html()
    cities = get_city_list(raw_html)
    engine = create_engine(connectStr, max_overflow=5)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        session.add_all(cities)
        session.commit()
    except Exception:
        session.rollback()
    finally:
        session.close()


if __name__ == '__main__':
    main()
