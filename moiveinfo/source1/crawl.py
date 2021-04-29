from selenium import webdriver
from tqdm import tqdm
import time

path = "F:\\projects\\python projects\\moiveinfo\\html_source\\{}.html"
url = "https://www.boxofficemojo.com/chart/ww_top_lifetime_gross/?area=XWW&offset={}"


def main():
    pages = 86
    driver = webdriver.PhantomJS()
    for index in tqdm(range(pages)):
        driver.get(url.format(str(index * 200)))
        time.sleep(3)
        with open(path.format(str(index)), "w", encoding="utf-8") as f:
            f.write(driver.page_source)


if __name__ == '__main__':
    main()
