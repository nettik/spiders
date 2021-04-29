from functools import wraps
import time

from source2.classes.ThreadPool import ThreadPool
from source2.crawl_moive_link import get_moive_link


def cal_time(func):
    @wraps(func)
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        print("\r" + str(round((end - start) / 60, 1)) + "分钟")

    return wrapper


@cal_time
def main():
    links_list = get_moive_link()
    thread_pool = ThreadPool(8)
    for item in links_list:
        thread_pool.put_task(item)
    thread_pool.create_and_start_thread()
    thread_pool.wait_all_task_done()


if __name__ == '__main__':
    main()

# header = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "accept-encoding": "gzip, deflate, br",
#     "accept-language": "zh-CN,zh;q=0.9",
#     "cache-control": "max-age=0"
# }

# info_pattern = re.compile('<div class="per_txt fr">(.*?)</div>', re.S)
# line_pattern = re.compile('<div class="txt_bottom_item">(.*?)</div></div>', re.S)
# name_pattern = re.compile('<h1>.*?<div>(.*?)</div>', re.S)
# director_pattern = re.compile('<a.*?>(.*?)</a>', re.S)
# editor_pattern = re.compile('<a.*?>(.*?)</a>', re.S)
# leading_role_pattern = re.compile('<a.*?>(.*?)</a>', re.S)
# moive_type_pattern = re.compile('<div class="txt_bottom_r">(.*?)</div>', re.S)
# region_pattern = re.compile('<div class="txt_bottom_r">(.*?)</div>', re.S)
# language_pattern = re.compile('<div class="txt_bottom_r">(.*?)</div>', re.S)
# date_pattern = re.compile('<div class="txt_bottom_r">.*?(\d{4}-\d{2}-\d{2}).*?</div>', re.S)
# duration_pattern = re.compile('<div class="txt_bottom_r">(.*?)</div>', re.S)


# def test():
#     try:
#         r = requests.get("https://www.imdb.cn/title/tt4852128/", headers=header, timeout=3)
#         r.raise_for_status()
#         r.encoding = "utf-8"
#         html = r.text
#         soup = BeautifulSoup(html, 'html5lib')
#         info = soup.find('div', attrs={'class': 'per_txt'}).prettify()
#         if info is not None:
#             lines_soup = BeautifulSoup(info, 'html5lib')
#             lines = lines_soup.find_all('div', attrs={'class': "txt_bottom_item"})
#             name = re.search(name_pattern, info).group(1)
#             for line in lines:
#                 line_html = line.prettify()
#                 if "导演" in line_html:
#                     director = re.search(director_pattern, line_html).group(1)
#                 elif "编剧" in line_html:
#                     editor = editor_pattern.findall(line_html)
#                 elif "主演" in line_html:
#                     leading_role = leading_role_pattern.findall(line_html)
#                 elif "类型" in line_html:
#                     moive_type = re.search(moive_type_pattern, line_html).group(1)
#                 elif "制片国家/地区" in line_html:
#                     region = re.search(region_pattern, line_html).group(1)
#                 elif "语言" in line_html:
#                     language = re.search(language_pattern, line_html).group(1)
#                 elif "片长" in line_html:
#                     duration = re.search(duration_pattern, line_html).group(1)
#                 elif "上映日期" in line_html:
#                     date = re.search(date_pattern, line_html).group(1)
#     except Exception as e:
#         print(e)
