import Errors
import pickle
import os
import Config

from MyEpisodes import MyEpisodes
# from TV_DB import TVDB_Class
from Series import Series
from Date import Date
import Helpers
import threading

class SeriesDataBase:

    ALL_SHOWS_UPDATE_TIME = 20  #days
    SERIES_UPDATE_TIME = 1

    # SERIES_UPDATE_TIME = 0

    def __init__(self):

        self.dic_of_series_in_db = {}  # show_name : series_object
        self.all_shows_last_update = None
        self.all_shows_dic = {}  # show_name : show_id

        self.series_last_update = None

        self.my_episodes = MyEpisodes()

    def get_series_object(self,series_name):
        series_name = series_name.lower()

        if series_name not in self.dic_of_series_in_db:
            raise Errors.ShowNotInDataBase

        series_obj = self.dic_of_series_in_db[series_name]
        return series_obj

    def add_new_show(self,show_name):
        show_name = show_name.lower()
        if show_name not in self.all_shows_dic:
            raise Errors.ShowNotInDataBase(show_name)

        if show_name in self.dic_of_series_in_db:
            return

        new_series = Series(show_name)
        self.dic_of_series_in_db[show_name] = new_series


    def save_series_data_base(self):
        Helpers.dump_to_pickle_object(Config.SERIES_DATA_BASE_FILE_PATH,self)

    def check_if_all_shows_dic_needs_update(self):

        ans = False
        num_of_days_since_last_update = Date().get_num_of_date_since(self.all_shows_last_update)
        if num_of_days_since_last_update > self.ALL_SHOWS_UPDATE_TIME:
            ans = True
        return ans

    def check_if_series_dic_needs_update(self):

        ans = False
        num_of_days_since_last_update = Date().get_num_of_date_since(self.series_last_update)
        if num_of_days_since_last_update > self.ALL_SHOWS_UPDATE_TIME:
            ans = True
        return ans

    def update_all_shows_dic(self):

        if self.all_shows_last_update:
            if not self.check_if_all_shows_dic_needs_update():
                return

        print "Updating all shows data base"

        try:
            string = "#abcdefghijklmnopqrstuvwxyz"

            for letter in string:
                shows_by_letters = MyEpisodes.get_all_shows_by_letter(letter)
                for show in shows_by_letters:
                    if show not in self.all_shows_dic:
                        self.all_shows_dic[show] = MyEpisodes.SHOW_NOT_FOUND

            self.all_shows_last_update = Date.get_now_time()

        except Exception as ex:
            Errors.CouldNotUpdateShows()


    def update_data_base(self):

        if self.series_last_update:
            if not self.check_if_series_dic_needs_update():
                return

        new_threads = []
        for series in self.dic_of_series_in_db.values():
            new_thread = threading.Thread(target=series.update_series_details)
            new_threads.append(new_thread)
            new_thread.start()

        for t in new_threads:
            t.join()

