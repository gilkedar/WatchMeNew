
from User import User
from UsersDataBase import UsersDataBase
from SeriesDataBase import SeriesDataBase
from Series import Series
from Date import Date
from Helpers import timeit
from ThePirateBay import PirateBay


import Errors
from MyEpisodes import MyEpisodes
import Config
import pickle
import os
from IMDB import IMDB_Class

SERIES_1 = "Narcos"
SERIES_2 = "Stranger Things"
SERIES_3 = "Modern Family"
SEASON_NUM = 2
EP_NUM = 3

class Session:

    def __init__(self,user=None,series_db=None):

        self.user = user
        self.series_db = series_db
        self.start_time = Date.get_now_time()

    def prepare_session(self):

        self.series_db.update_data_base()
        self.series_db.update_all_shows_dic()

    def create_torrent_sites(self):
        PirateBay()

    def simulate_session(self):

        self.create_torrent_sites()

        self.add_series(SERIES_1)
        self.add_series(SERIES_2)
        self.add_series(SERIES_3)

        self.download_episode(SERIES_1,SEASON_NUM,EP_NUM)

        # season_item = self.series_db[SERIES_1][SEASON_NUM]
        # season_item.download()
        #


    # def save_series_data_base(self):
    #     file_ob = open(Config.SERIES_DATA_BASE_FILE_PATH, "w")
    #     pickle.dump(self.series_db, file_ob)
    #     file_ob.close()

    # def update_user_series(self):
    #     for series in self.user.lst_of_series:
    #         series_obj = self.series_db[series]
    #         # series_obj.update_series_details()



    def add_series(self,series_name):
        self.series_db.add_new_show(series_name)
        self.user.add_series(series_name)

    def download_episode(self,series_name,season_num,ep_num):
        series_obj = self.series_db.get_series_object(series_name)
        episode_item = series_obj.get_episode_object(season_num,ep_num)
        episode_item.get_lst_of_options()
        best_torrent = episode_item.choose_best_option()
        best_torrent.download()