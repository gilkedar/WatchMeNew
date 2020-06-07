
from TorrentSite import TorrentSite
from bs4 import BeautifulSoup
from Torrent import Torrent
from Errors import PirateBayError


class PirateBay(TorrentSite):

    def __init__(self):

        TorrentSite.__init__(self,"The Pirate Bay","http://thepiratebay.org")

    def get_list_of_torrents(self,item_object):

        try:
            item = item_object.name.replace('\'', '')
            if ' (us)' in item:
                show = item.replace(' (us)', '')
            self.url += '/search/' + item + '/0/99/0'
            data = self.read_webSite()
            html = data.lower()
            str = '<div class="detname">'  # parsing file to find 720P quality
            torrents_list = html.split(str)
            default_magnet = ''
            default_name = ''
            default_release = ''
            counter = 0

            valid_torrents = []
            for torrent_data in torrents_list[1:]:
                if len(valid_torrents) == self.num_of_torrents_to_find:
                    break

                counter += 1
                end_of_name_data = torrent_data.find('</div>')
                name_data = torrent_data[:end_of_name_data - 5]
                torrent_name = name_data[name_data.rfind('>') + 1:].lower()
                seeders_idx = torrent_data.find('<td align="right">')
                num_of_seeders = torrent_data[seeders_idx + 18: torrent_data.find('</td>', seeders_idx)]

                if num_of_seeders < self.min_seeders:
                    break
                magnet_index = torrent_data.find('magnet:')
                magnet_link = torrent_data[magnet_index: torrent_data.find('"', magnet_index + 7)]

                curr_torrent = Torrent(item_object.name, item_object.type, torrent_name,num_of_seeders,magnet_link)
                if curr_torrent.check_if_valid():
                    valid_torrents.append(curr_torrent)

            return valid_torrents

        except Exception as ex:
            raise PirateBayError(item)
