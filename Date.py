import datetime


class Date:

    def __init__(self):

        self.date = datetime.datetime.today()

    def to_string(self,date):

        new_date = str(date.day) + '-' + str(date.month) + '-' + str(date.year)
        return new_date

    def get_num_of_days_since_my_date(self):
        today = datetime.datetime.today() - datetime.timedelta(hours=7)
        start = self.date
        # start = datetime.datetime.strptime(since, "%d-%m-%Y")
        date_generated = [start + datetime.timedelta(days=x) for x in range(0, (today - start).days)]
        return len(date_generated)

    @staticmethod
    def get_now_time():
        return str(datetime.datetime.now())


    @staticmethod
    def get_lst_of_date_since(since):

        today = datetime.datetime.today() - datetime.timedelta(hours=7)
        start = since.date
        # start = datetime.datetime.strptime(since, "%d-%m-%Y")
        date_generated = [start + datetime.timedelta(days=x) for x in range(0, (today - start).days)]
        return date_generated

    @staticmethod
    def get_num_of_date_since(since):

        today = datetime.datetime.today() - datetime.timedelta(hours=7)
        start = since.date
        # start = datetime.datetime.strptime(since, "%d-%m-%Y")
        date_generated = [start + datetime.timedelta(days=x) for x in range(0, (today - start).days)]
        return len(date_generated)