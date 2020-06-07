
from Website import Website
import Config


class TorrentSite(Website):

    lst_of_torrent_sites = []

    def __init__(self,name,adress):
        Website.__init__(self,adress)
        self.name = name
        self.lst_of_torrent_sites.append(self)
        self.num_of_torrents_to_find = Config.NUM_OF_TORRENTS_TO_FIND
        self.min_seeders = Config.NUM_OF_IN_SEEDERS

    def get_list_of_torrents(self,search_name):
        pass


