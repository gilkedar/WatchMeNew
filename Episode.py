from Item import Item
from TorrentSite import TorrentSite


class Episode(Item):

    def __init__(self,series_name,season_number, episode_number,episode_name,release_date):

        episode_str = "{} s{}e{}".format(series_name,season_number,episode_number)
        Item.__init__(self,Episode.__name__,episode_str)
        self.season_num = season_number
        self.episode_num = episode_number
        self.episode_name = episode_name
        self.release_date = release_date
        # self.agg_num =  agg_series_num
        self.aquired = None
        self.watched = None
        self.released = False

    def get_lst_of_options(self):

        for torrent_site in TorrentSite.lst_of_torrent_sites:
            self.lst_of_options += torrent_site.get_list_of_torrents(self)
            if len(self.lst_of_options) >= torrent_site.num_of_torrents_to_find:
                break


    def choose_best_option(self):
        return self.lst_of_options[0] # return first option

