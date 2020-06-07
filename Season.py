
from Item import Item


class Season(Item):

    def __init__(self,series_name,season_num,epsisodes_lst):
        season_str = "{} s{}".format(series_name,season_num)
        Item.__init__(self, season_str, Season.__name__)
        self.season_num = season_num
        self.episodes_lst = epsisodes_lst
        self.release_date = epsisodes_lst['01'].release_date
        self.image = None


    def download_season(self):
        pass

