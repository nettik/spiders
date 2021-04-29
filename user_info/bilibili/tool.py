from selenium import webdriver
import time
import json


def save_cookie():
    driver = webdriver.Chrome()
    time.sleep(10)
    url = "https://passport.bilibili.com/login"
    driver.get(url)
    driver.maximize_window()
    time.sleep(60)
    cookies = driver.get_cookies()
    with open("data/cookies.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(cookies, ensure_ascii=False))


def load_cookie():
    with open("data/cookies.json", "r", encoding="utf-8") as f:
        cookies = json.loads(f.read())
    result = list()
    for item in cookies:
        result.append({
            "name": item["name"],
            "value": item["value"]
        })
    return result


if __name__ == '__main__':
    save_cookie()
