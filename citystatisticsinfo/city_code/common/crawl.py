import requests
import traceback
import re
import cchardet

root_url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/"

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Host": "www.stats.gov.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
}

province_line_pattern = re.compile("<tr class='provincetr'>(.*?)</tr>", re.S)
province_pattern = re.compile("<a href='(.*?)'>(.*?)</a>", re.S)


# 省
def crawl_province():
    result = list()
    try:
        r = requests.get(root_url, headers=header, timeout=6)
        r.raise_for_status()
        r.encoding = cchardet.detect(r.content)["encoding"]
        html = r.text
        province_lines = province_line_pattern.findall(html)
        if len(province_lines) > 0:
            for line in province_lines:
                provinces = province_pattern.findall(line)
                for item in provinces:
                    result.append({
                        "name": item[1].replace("<br/>", ""),
                        "code": item[0].replace(".html", ""),
                        "province_link": item[0]
                    })
        return result
    except:
        traceback.print_exc()
        return None


city_line_pattern = re.compile("<tr class='citytr'>(.*?)</tr>", re.S)
city_link_pattern = re.compile("<a href='(.*?)'>")
city_name_code_pattern = re.compile("<a.*?>(.*?)</a>", re.S)


# 市
def crawl_city(province_link):
    result = list()
    url = "".join([root_url, province_link])
    try:
        r = requests.get(url, headers=header, timeout=6)
        r.raise_for_status()
        r.encoding = cchardet.detect(r.content)["encoding"]
        html = r.text
        city_lines = city_line_pattern.findall(html)
        if len(city_lines) > 0:
            for line in city_lines:
                link = re.search(city_link_pattern, line).group(1)
                name_code = city_name_code_pattern.findall(line)
                result.append({
                    "name": name_code[1],
                    "code": name_code[0],
                    "city_link": link
                })
        return result
    except:
        traceback.print_exc()
        return None


county_line_pattern = re.compile("<tr class='countytr'>(.*?)</tr>", re.S)
county_col_pattern = re.compile("<td>(.*?)</td>", re.S)
county_link_pattern = re.compile("<a href='(.*?)'>")
county_name_code_pattern = re.compile("<a.*?>(.*?)</a>", re.S)


# 县区
def crawl_county(city_link):
    result = list()
    url = "".join([root_url, city_link])
    try:
        r = requests.get(url, headers=header, timeout=6)
        r.raise_for_status()
        r.encoding = cchardet.detect(r.content)["encoding"]
        html = r.text
        county_lines = county_line_pattern.findall(html)
        if len(county_lines) > 0:
            for line in county_lines:
                cols = county_col_pattern.findall(line)
                if len(cols) > 0:
                    link_t = re.search(county_link_pattern, cols[0])
                    if link_t is None:
                        result.append({
                            "name": cols[1],
                            "code": cols[0],
                            "county_link": ""
                        })
                    else:
                        result.append({
                            "name": re.search(county_name_code_pattern, cols[1]).group(1),
                            "code": re.search(county_name_code_pattern, cols[0]).group(1),
                            "county_link": link_t.group(1)
                        })
        return result
    except:
        traceback.print_exc()
        return None


street_line_pattern = re.compile("<tr class='towntr'>(.*?)</tr>", re.S)
street_col_pattern = re.compile("<td>(.*?)</td>", re.S)
street_link_pattern = re.compile("<a href='(.*?)'>")
street_name_code_pattern = re.compile("<a.*?>(.*?)</a>", re.S)


# 街道
def crawl_street(province_code, county_link):
    result = list()
    url = "".join([root_url, province_code, county_link])
    try:
        r = requests.get(url, headers=header, timeout=6)
        r.raise_for_status()
        r.encoding = cchardet.detect(r.content)["encoding"]
        html = r.text
        street_lines = street_line_pattern.findall(html)
        if len(street_lines) > 0:
            for line in street_lines:
                cols = street_col_pattern.findall(line)
                if len(cols) > 0:
                    link_t = re.search(street_link_pattern, cols[0])
                    if link_t is None:
                        result.append({
                            "name": cols[1],
                            "code": cols[0],
                            "county_link": ""
                        })
                    else:
                        result.append({
                            "name": re.search(street_name_code_pattern, cols[1]).group(1),
                            "code": re.search(street_name_code_pattern, cols[0]).group(1),
                            "street_link": link_t.group(1)
                        })
        return result
    except:
        traceback.print_exc()
        return None


neighborhood_line_pattern = re.compile("<tr class='villagetr'>(.*?)</tr>", re.S)
neighborhood_col_pattern = re.compile("<td>(.*?)</td>", re.S)


# 居委会
def crawl_neighborhood(province_code, county_link, street_link):
    url = "".join([root_url, province_code, county_link.split("/")[0] + "/", street_link])
    result = list()
    try:
        r = requests.get(url, headers=header, timeout=6)
        r.raise_for_status()
        r.encoding = cchardet.detect(r.content)["encoding"]
        html = r.text
        neighborhood_lines = neighborhood_line_pattern.findall(html)
        if len(neighborhood_lines) > 0:
            for line in neighborhood_lines:
                cols = neighborhood_col_pattern.findall(line)
                if len(cols) > 0:
                    result.append({
                        "name": cols[2],
                        "code": cols[0]
                    })
        return result
    except:
        traceback.print_exc()
        return None


if __name__ == '__main__':
    pass
    # crawl_province()
    # crawl_city("31.html")
    # crawl_county('32/3201.html')
    # crawl_street("32/", '01/320102.html')
    # crawl_neighborhood("32/", '01/320102.html', '02/320102002.html')
