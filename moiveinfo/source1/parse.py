import os
import pandas
from tqdm import tqdm
from source1.classes.Tool import Tool

path = "F:\\projects\\python projects\\moiveinfo\\html_source"
header = ["排名", "电影名称", "总票房(美元)", "上映时间"]


def main():
    files = os.listdir(path)
    result = []
    for file in tqdm(files):
        with open(path + "\\" + file, "r", encoding="utf-8") as f:
            html = f.read()
        tbody = Tool.tbody_pattern.findall(html)[0]
        tr_list = Tool.tr_pattern.findall(tbody)
        for tr in tr_list:
            tds = Tool.td_pattern.findall(tr)
            rank = int(tds[0].replace(",", ""))
            title = Tool.title_pattern.findall(tds[1])[0]
            worldwide_lifetime_gross = tds[2].lstrip("$").replace(",", "")
            year = Tool.year_pattern.findall(tds[7])[0]
            result.append([rank, title, worldwide_lifetime_gross, year])
    df = pandas.DataFrame(result)
    df.to_excel("moive.xls", index=False, header=header)


if __name__ == '__main__':
    main()
