
from Series import Series
from SeriesDataBase import SeriesDataBase
from Date import Date
import Errors
import Helpers
import Config

from Config import ConfigClass

import threading
class User:

    def __init__(self,user_name,password):

        self.user_name = user_name
        self.password = password
        self.id = 0
        self.favorite_shows = None
        self.last_visit = None
        self.lst_of_series = []

        self.userConfig = ConfigClass()
        self.set_last_visit()

    def get_lst_of_shows(self):
        return self.lst_of_series

    def set_last_visit(self):
        self.last_visit = Date()


    def get_last_visit_date(self):
        return self.last_visit

    def days_from_last_visit(self):

        self.last_visit.get_num_of_date_since(self.last_visit)

    def update_password(self):
        pass

    def add_series(self,series):

        self.lst_of_series.append(series)

