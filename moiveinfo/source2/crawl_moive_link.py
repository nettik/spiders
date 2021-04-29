import re
import traceback
import time

import cchardet
import requests
from tqdm import tqdm

root_url = "https://www.imdb.cn/feature-film/"
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0"
}
pages = 200

all_links_pattern = re.compile('<ul class="hot_list">(.*?)</ul>', re.S)
link_pattern = re.compile('<a class="img_box" href="(.*?)".*?>', re.S)


def crawl_page(para):
    param = {
        "page": para
    }
    try:
        r = requests.get(root_url, headers=header, timeout=12, params=param)
        r.raise_for_status()
        encoding = cchardet.detect(r.content)["encoding"]
        r.encoding = encoding
        return r.text
    except Exception as e:
        print("error: page" + str(para))
        traceback.print_exc()
        return None


def get_links(html):
    all_links = re.search(all_links_pattern, html).group()
    if all_links is not None:
        return link_pattern.findall(all_links)
    return None


def get_moive_link():
    result = list()
    for param in tqdm(range(pages)):
        html = crawl_page(param + 1)
        time.sleep(1)
        if html is not None:
            all_links = get_links(html)
            if all_links is not None:
                result.extend(all_links)
    return result
