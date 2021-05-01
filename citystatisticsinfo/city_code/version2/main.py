from city_code.common.crawl import crawl_province, crawl_city, crawl_county, crawl_street, crawl_neighborhood
import json
from tqdm import tqdm
import time


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


def main():
    save_county_in_file()


if __name__ == '__main__':
    main()
