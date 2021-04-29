import re


class Tool:
    name_pattern = re.compile('<h1>(.*?)<span>.*?</span></h1>', re.DOTALL)
    id_pattern = re.compile('<h1>.*?<span>\((.*?)\)</span>.*?</h1>', re.DOTALL)
    type_pattern = re.compile('<p class="risk">.*?<span>(.*?)</span>.*?</p>', re.DOTALL)
    tag_str_pattern = re.compile('<ul class="fund_tags .*?">(.*?)</ul>', re.DOTALL)
    tag_pattern = re.compile('<li>(.*?)</li>')
    build_time_pattern = re.compile('<li>.*?成立时间.*?<span>(.*?)</span>.*?</li>', re.DOTALL)
    latest_scale_pattern = re.compile('<li>.*?最新规模.*?<span>(.*?)</span>.*?</li>', re.DOTALL)
    income_str_pattern = re.compile('<div .*? id="nTab9_0".*?>.*?<td class="t-bg">区间回报</td>(.*?)</tr>.*?</div>',
                                    re.DOTALL)
    income_pattern = re.compile('<td class="to-right">(.*?)</td>')
    income_rate_pattern = re.compile('<span.*?>(.*?)</span>')
    sharp_rate_str_pattern = re.compile('<div class="fxzb">.*?<td.*?>年化夏普比率</td>(.*?)</tr>', re.DOTALL)
    sharp_rate_pattern = re.compile('<td.*?>(.*?)</td>', re.DOTALL)

    # 持股持债比例
    cgczbl_pattern = re.compile("gpzhListData = ({.*?});")
    # 资产配置
    zcpz_pattern = re.compile("hyPieData = ({.*?});")
    # 行业配置
    hypz_pattern = re.compile("zcPieData = ({.*?});")

    html_url_pattern = "https://www.howbuy.com/fund/{}/"

    html_header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Referer': 'https://www.howbuy.com/fund/trade/',
        'Host': 'www.howbuy.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    js_url_pattern = "https://static.howbuy.com/??/upload/auto/script/fund/jzzs_{}.js,/upload/auto/script/fund/jjjl_{}.js,/upload/auto/script/fund/data_{}.js"

    js_header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Referer': 'https://www.howbuy.com/',
        'Host': 'static.howbuy.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': '*/*'
    }

    # 指数型、QDII、混合型、股票型
    @staticmethod
    def replace_cgczbl_stock(cgczbl):
        return cgczbl.replace("\'", "\"").replace("zqmc", "\"zqmc\"").replace("zqdm", "\"zqdm\"").replace("zjbl",
                                                                                                          "\"zjbl\"").replace(
            "ccdb", "\"ccdb\"").replace("jsrq", "\"jsrq\"").replace("cgjzdList", "CgjzdList").replace("cgjzd",
                                                                                                      "\"cgjzd\"")

    # 债券型
    @staticmethod
    def replace_cgczbl_bond(cgczbl):
        return cgczbl.replace("\'", "\"").replace("zqmc", "\"zqmc\"").replace("zqdm", "\"zqdm\"").replace("zjbl",
                                                                                                          "\"zjbl\"").replace(
            "ccdb", "\"ccdb\"").replace("jsrq", "\"jsrq\"").replace("czjzdList", "CzjzdList").replace("czjzd",
                                                                                                      "\"czjzd\"")

    @staticmethod
    def replace_zcpz(zcpz):
        return zcpz.replace("\'", "\"").replace("name", "\"name\"").replace("y", "\"y\"")

    @staticmethod
    def replace_hypz(hypz):
        return hypz.replace("\'", "\"").replace("jjzc", "\"jjzc\"").replace("data", "\"data\"").replace("name",
                                                                                                        "\"name\"").replace(
            "tly", "\"x\"").replace("y", "\"y\"")
