from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from source1.po import CityInfo
import pandas as pd

connectStr = "mysql+pymysql://root:root@localhost:3306/weatherinfodb"
engine = create_engine(connectStr, max_overflow=5)
Session = sessionmaker(bind=engine)
session = Session()


def read_file():
    file_path = "C:\\Users\\YL\\Desktop\\LocationList-master\\China-City-List-latest.csv"
    data = pd.read_csv(file_path, header=0)
    return data.values.tolist()


def save(city_info):
    result = []
    for city in city_info:
        result.append(
            CityInfo(
                city[0], city[1], city[2], city[3],
                city[4], city[5], city[6], city[7],
                city[8], city[9], city[10], city[11]
            )
        )
    session.execute("delete from city_info")
    session.commit()
    session.add_all(result)
    session.commit()
    session.close()


def update():
    try:
        city_info = read_file()
        save(city_info)
    except:
        pass


if __name__ == '__main__':
    update()
