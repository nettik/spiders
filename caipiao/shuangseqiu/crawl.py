import re
import requests
import cchardet
from tqdm import tqdm
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import time
import pandas
from shuangseqiu.classes.TwoColorBall import TwoColorBall

file_path = "D:\\6-baiduyun\\2-数据\\5-彩票\\双色球.xls"
header_list = ["期号", "日期", "红球1", "红球2", "红球3", "红球4", "红球5", "红球6",
               "蓝球", "本期销量/元", "奖池滚存/元", "一等奖注数", "一等奖单注奖金/元",
               "二等奖注数", "二等奖单注奖金/元", "三等奖注数", "三等奖单注奖金/元"]

date_pattern = re.compile('开奖日期.*?\d{4}年\d{1,2}月\d{1,2}日', re.DOTALL)
red_pattern = re.compile('<li class="ball_red">(\d{2})</li>')
blue_pattern = re.compile('<li class="ball_blue">(\d{2})</li>')
sale_pattern = re.compile('本期销量.*?>(.*?)元', re.DOTALL)
pool_pattern = re.compile('奖池滚存.*?>(.*?)元', re.DOTALL)
first_pattern = re.compile('<tr align="center">\s+<td>\s+一等奖.*?</tr>', re.DOTALL)
second_pattern = re.compile('<tr align="center">\s+<td>\s+二等奖.*?</tr>', re.DOTALL)
third_pattern = re.compile('<tr align="center">\s+<td>\s+三等奖.*?</tr>', re.DOTALL)
num_pattern = re.compile('<td>\s+(.*?)</td>')

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "referer": "https://kaijiang.500.com/",
    "cache-control": "max-age=0",
    "accept-language": "zh-CN,zh;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

connectStr = "mysql+pymysql://root:root@localhost:3306/caipiaoinfodb"
engine = create_engine(connectStr, max_overflow=5)
Session = sessionmaker(bind=engine)


def crawl(url):
    try:
        r = requests.get(url, headers=headers, timeout=12)
        r.raise_for_status()
        encoding = cchardet.detect(r.content)
        r.encoding = encoding["encoding"]
        return r.text
    except:
        return ""


def getParam():
    root_url = "https://kaijiang.500.com/ssq.shtml"
    try:
        r = requests.get(root_url, headers=headers, timeout=6)
        r.raise_for_status()
        encoding = cchardet.detect(r.content)
        r.encoding = encoding
        div_pattern = re.compile('<div class="iSelectList">(.*?)</div>', re.DOTALL)
        div = div_pattern.findall(r.text)[0]
        link_pattern = re.compile('(\d+?).shtml')
        return link_pattern.findall(div)
    except Exception as e:
        print(e)
    return list()


def main():
    session = Session()
    params = getParam()[0:18]
    url_pattern = "https://kaijiang.500.com/shtml/ssq/{}.shtml"
    for param in tqdm(params):
        page = crawl(url_pattern.format(param))
        time.sleep(0.5)
        if page != "":
            two_color_ball = TwoColorBall(param)
            date_t = date_pattern.findall(page)
            if len(date_t) > 0:
                two_color_ball.date = date_t[0].split('：')[-1]
            red_t = red_pattern.findall(page)
            if len(red_t) > 0:
                two_color_ball.red1 = red_t[0]
                two_color_ball.red2 = red_t[1]
                two_color_ball.red3 = red_t[2]
                two_color_ball.red4 = red_t[3]
                two_color_ball.red5 = red_t[4]
                two_color_ball.red6 = red_t[5]
            blue_t = blue_pattern.findall(page)
            if len(blue_t) > 0:
                two_color_ball.blue = blue_t[0]
            sale_t = sale_pattern.findall(page)
            if len(sale_t) > 0:
                two_color_ball.sale_money = sale_t[0].replace(",", "")
            pool_t = pool_pattern.findall(page)
            if len(pool_t) > 0:
                two_color_ball.pool_money = pool_t[0].replace(",", "")
            first_prize_t = first_pattern.findall(page)
            if len(first_prize_t) > 0:
                num1 = num_pattern.findall(first_prize_t[0])
                two_color_ball.first_prize_num = num1[1].replace(",", "")
                two_color_ball.first_prize_money = num1[2].replace(",", "")
            second_prize_t = second_pattern.findall(page)
            if len(second_prize_t) > 0:
                num2 = num_pattern.findall(second_prize_t[0])
                two_color_ball.second_prize_num = num2[1].replace(",", "")
                two_color_ball.second_prize_money = num2[2].replace(",", "")
            third_prize_t = third_pattern.findall(page)
            if len(third_prize_t) > 0:
                num3 = num_pattern.findall(third_prize_t[0])
                two_color_ball.third_prize_num = num3[1].replace(",", "")
                two_color_ball.third_prize_money = num3[2].replace(",", "")
            try:
                session.add(two_color_ball)
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
    save_in_file(session)


def save_in_file(session):
    data_list = session.query(TwoColorBall).all()
    data = [item.to_list() for item in data_list]
    df = pandas.DataFrame(data)
    df.to_excel(file_path, index=False, header=header_list)


if __name__ == '__main__':
    main()
