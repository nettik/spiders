class FundManager(object):
    def __init__(self):
        self.manager_name = ""
        self.manager_work_time = ""
        self.average_income_rate_per_work_year = 0.0
        self.max_increase_rate = 0.0
        self.max_decrease_rate = 0.0

    def to_insert_sql(self):
        return "'" + self.manager_name + "'" + ',' + \
               "'" + self.manager_work_time + "'" + ',' + \
               str(self.average_income_rate_per_work_year) + ',' + \
               str(self.max_increase_rate) + ',' + \
               str(self.max_decrease_rate)
