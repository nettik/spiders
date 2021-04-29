from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
from source1.po.WeatherInfoPerDay import WeatherInfoPerDay
import pandas

weather_info_headers = [
    "行政区ID", "行政区名称", "所属国家", "所属一级行政区", "所属二级行政区", "纬度", "经度",
    "日期", "日出时间", "日落时间", "月升时间", "月落时间", "月相名称", "最高温度", "最低温度", "白天天气状况",
    "晚间天气状况", "白天风向360角度", "白天风向", "白天风力等级", "白天风速，公里/小时", "夜间风向360角度",
    "夜间当天风向", "夜间风力等级", "夜间风速", "相对湿度", "降水量", "大气压强", "能见度", "云量，百分比数值", "紫外线强度指数",
]


class GetWeatherInfo:
    connectStr = "mysql+pymysql://root:root@localhost:3306/weatherinfodb"
    engine = create_engine(connectStr, max_overflow=5)
    Session = sessionmaker(bind=engine)
    session = Session()

    def __init__(self, key, url):
        self.key = key
        # https://devapi.qweather.com/v7/weather/3d?{请求参数}
        # https://devapi.qweather.com/v7/weather/7d?{请求参数}
        self.url = url
        self.weather_data = []

    def __del__(self):
        self.session.close()

    def save_in_file(self, date, file_path):
        file_name = file_path.format(date)
        sql = "SELECT * FROM city_weather_forcast WHERE city_weather_forcast.date = '{}'".format(date)
        data = self.engine.execute(sql).fetchall()
        data_frame = pandas.DataFrame(data)
        data_frame.to_excel(file_name, encoding='utf-8', index=False, header=weather_info_headers)

    def get_weather_info(self, locaiontId):
        self.weather_data.clear()
        url = self.url + "key=" + self.key + "&location=" + locaiontId
        response = requests.get(url)
        response.encoding = 'utf-8'
        data = response.json()
        if data["code"] == "200":
            forcast_info = data["daily"]
            for info in forcast_info:
                obj_weather_info = WeatherInfoPerDay(
                    locaiontId,
                    info["fxDate"], info["sunrise"], info["sunset"],
                    info["moonrise"], info["moonset"],
                    info["moonPhase"], info["tempMax"], info["tempMin"], info["textDay"],
                    info["textNight"], info["wind360Day"], info["windDirDay"],
                    info["windScaleDay"], info["windSpeedDay"], info["wind360Night"], info["windDirNight"],
                    info["windScaleNight"], info["windSpeedNight"],
                    info["humidity"], info["precip"], info["pressure"], info["vis"],
                    info["cloud"], info["uvIndex"],
                )
                self.weather_data.append(obj_weather_info)
            try:
                self.session.add_all(self.weather_data)
                self.session.commit()
            except:
                self.session.rollback()
