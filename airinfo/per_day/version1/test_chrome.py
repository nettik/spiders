from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver import Chrome


def main():
    url = "https://www.aqistudy.cn/historydata/monthdata.php?city=北京"
    global driver
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    # chrome_option = Options()
    # chrome_option.add_argument('headless')
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    time.sleep(10)
    driver.get(url)
    time.sleep(5)
    with open("data.html", "w") as f:
        f.write(driver.page_source)


if __name__ == '__main__':
    main()
