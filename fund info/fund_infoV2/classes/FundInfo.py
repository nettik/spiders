class FundInfo(object):
    def __init__(self):
        self.fund_name = ""
        self.fund_id = ""
        self.fund_type = ""
        self.fund_tags = ""
        self.build_time = ""
        self.latest_scale = ""
        self.since_this_year_rate = 0.0
        self.last_one_week_rate = 0.0
        self.last_one_month_rate = 0.0
        self.last_three_month_rate = 0.0
        self.last_six_month_rate = 0.0
        self.last_one_year_rate = 0.0
        self.last_two_year_rate = 0.0
        self.last_three_year_rate = 0.0
        self.manager_name = ""
        self.manager_work_time = ""
        self.average_income_rate_per_work_year = 0.0
        self.max_increase_rate = 0.0
        self.max_decrease_rate = 0.0

    def to_insert_sql(self):
        return "'" + self.fund_id + "'" + ',' + \
               "'" + self.fund_name + "'" + ',' + \
               "'" + self.fund_type + "'" + ',' + \
               "'" + self.fund_tags + "'" + ',' + \
               "'" + self.build_time + "'" + ',' + \
               "'" + self.latest_scale + "'" + ',' + \
               str(self.since_this_year_rate) + ',' + \
               str(self.last_one_week_rate) + ',' + \
               str(self.last_one_month_rate) + ',' + \
               str(self.last_three_month_rate) + ',' + \
               str(self.last_six_month_rate) + ',' + \
               str(self.last_one_year_rate) + ',' + \
               str(self.last_two_year_rate) + ',' + \
               str(self.last_three_year_rate) + ',' + \
               "'" + self.manager_name + "'" + ',' + \
               "'" + self.manager_work_time + "'" + ',' + \
               str(self.average_income_rate_per_work_year) + ',' + \
               str(self.max_increase_rate) + ',' + \
               str(self.max_decrease_rate)
