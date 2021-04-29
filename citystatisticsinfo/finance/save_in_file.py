import pandas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from finance.classes.accommodation_dining import AccommodationDining
from finance.classes.agriculture import Agriculture
from finance.classes.construction import Construction
from finance.classes.finance import Finance
from finance.classes.gdp import Gdp
from finance.classes.industry import Industry
from finance.classes.primary import Primary
from finance.classes.secondary import Secondary
from finance.classes.tertiary import Tertiary
from finance.classes.transportation import Transportation
from finance.classes.wholesale_retail import WholesaleRetail

path = "D:\\6-baiduyun\\2-数据\\6-城市统计数据\\0-经济\\{}.xls"
connectStr = "mysql+pymysql://root:root@localhost:3306/citystatisticsinfodb"
engine = create_engine(connectStr, max_overflow=5)
Session = sessionmaker(bind=engine)


def data_per_classification():
    header_list = ["地区", "2019年", "2018年", "2017年", "2016年", "2015年", "2014年", "2013年",
                   "2012年", "2011年", "2010年", "2009年", "2008年", "2007年", "2006年", "2005年",
                   "2004年", "2004年", "2002年", "2001年", "2000年"]
    session = Session()
    # 地区生产总值
    pandas.DataFrame([item.to_list() for item in session.query(Gdp).all()]).to_excel(path.format("地区生产总值"), index=False,
                                                                                     header=header_list)
    # 第一产业增加值
    pandas.DataFrame([item.to_list() for item in session.query(Primary).all()]).to_excel(path.format("第一产业增加值"),
                                                                                         index=False,
                                                                                         header=header_list)
    # 第二产业增加值
    pandas.DataFrame([item.to_list() for item in session.query(Secondary).all()]).to_excel(path.format("第二产业增加值"),
                                                                                           index=False,
                                                                                           header=header_list)
    # 第三产业增加值
    pandas.DataFrame([item.to_list() for item in session.query(Tertiary).all()]).to_excel(path.format("第三产业增加值"),
                                                                                          index=False,
                                                                                          header=header_list)
    # 农林牧渔增加值
    pandas.DataFrame([item.to_list() for item in session.query(Agriculture).all()]).to_excel(path.format("农林牧渔增加值"),
                                                                                             index=False,
                                                                                             header=header_list)
    # 工业增加值
    pandas.DataFrame([item.to_list() for item in session.query(Industry).all()]).to_excel(path.format("工业增加值"),
                                                                                          index=False,
                                                                                          header=header_list)
    # 建筑业增加值
    pandas.DataFrame([item.to_list() for item in session.query(Construction).all()]).to_excel(path.format("建筑业增加值"),
                                                                                              index=False,
                                                                                              header=header_list)
    # 批发和零售业增加值
    pandas.DataFrame([item.to_list() for item in session.query(WholesaleRetail).all()]).to_excel(
        path.format("批发和零售业增加值"), index=False,
        header=header_list)
    # 交通运输仓储和邮政增加值
    pandas.DataFrame([item.to_list() for item in session.query(Transportation).all()]).to_excel(
        path.format("交通运输仓储和邮政增加值"), index=False,
        header=header_list)
    # 住宿和餐饮增加值
    pandas.DataFrame([item.to_list() for item in session.query(AccommodationDining).all()]).to_excel(
        path.format("住宿和餐饮增加值"), index=False,
        header=header_list)
    # 金融增加值
    pandas.DataFrame([item.to_list() for item in session.query(Finance).all()]).to_excel(path.format("金融增加值"),
                                                                                         index=False,
                                                                                         header=header_list)


def main():
    data_per_classification()


if __name__ == '__main__':
    main()
