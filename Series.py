from Item import Item
# from TV_DB import TVDB_Class
from MyEpisodes import MyEpisodes
from IMDB import IMDB_Class
import Errors
from Season import Season
from Episode import Episode

class Series():

    def __init__(self, name):

        self.series_name = name
        self.rating = None
        self.num_of_seasons = None
        self.current_season = None
        self.last_episode_released = None

        self.eps_dic = {}
        self.my_episodes_id = MyEpisodes.SHOW_NOT_FOUND
        self.imdb_url = None

        self.update_series_details()

    def get_num_of_seasons(self):

        num = len(self.eps_dic)
        return num

    def get_episodes(self):

        if self.my_episodes_id == MyEpisodes.SHOW_NOT_FOUND:
            self.my_episodes_id = MyEpisodes.get_show_id(self.series_name)

        self.eps_dic = MyEpisodes.get_episodes_from_ajax(self.series_name,self.my_episodes_id,self.eps_dic)

    def get_episode_object(self,season_num,episode_num):
        season_str = str(season_num).zfill(2)
        ep_str = str(episode_num).zfill(2)
        return self.eps_dic[season_str][ep_str]

    def get_current_season(self):
        season_lst = sorted(self.eps_dic.keys())
        last_season = None
        if  season_lst:
            last_season = season_lst[-1]
        return last_season

    def get_last_episode(self):
        last_ep = None
        if self.eps_dic:
            last_ep = sorted(self.eps_dic[self.current_season].keys())[-1]
        return last_ep


    def update_series_details(self):

        self.get_episodes()
        self.get_series_rating()
        self.num_of_seasons = self.get_num_of_seasons()
        self.current_season = self.get_current_season()
        self.last_episode_released = self.get_last_episode()

    def get_series_rating(self):

        if not self.imdb_url:
            self.imdb_url = IMDB_Class.get_imdb_url(self.series_name)

        self.rating = IMDB_Class.get_imdb_rating(self.imdb_url)

    def generate_season_item(self,season_num):

        episodes_lst = self.eps_dic[season_num].values()
        new_season = Season(self.series_name,season_num,episodes_lst)
        return new_season

    # def generate_episode_item(self,season_num,ep_num):
    #
    #     details = self.my_episodes.eps_dic[season_num][ep_num]
    #     new_episode = Episode(self.series_name,season_num,ep_num,details)
    #
    #
