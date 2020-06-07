from Website import Website
import os
import urllib2
import Helpers
import Errors
from bs4 import BeautifulSoup
import requests
import datetime
import Series
from Episode import Episode


class MyEpisodes:

    SHOW_NOT_FOUND = -1

    SHOW_ID_URL = "https://myepisodes.com/shows/"
    # shows_by_date_site = Website("https://www.myepisodes.com/epsbydate/")
    # episodes_by_id_site = Website("https://www.myepisodes.com/epsbyshow/")
    EPISODES_AJAX_URL = "https://www.myepisodes.com/ajax/service.php?mode=view_epsbyshow"

    show_id_dic = {}

    @staticmethod
    def has_id(series_name):
        ans = False
        if series_name in MyEpisodes.show_id_dic:
            id = MyEpisodes.show_id_dic[series_name]
            if id != MyEpisodes.SHOW_NOT_FOUND:
                ans = True
        return ans

    @staticmethod
    def get_episodes_from_ajax(series_name,show_id,eps_dic=None):

        # self.episodes_by_id_site.url += self.show_id
        # self.episodes_by_id_site.read_webSite()
        # show_id = MyEpisodes.SHOW_NOT_FOUND
        # if not MyEpisodes.has_id(series_name):
        #     show_id = MyEpisodes.get_show_id(series_name)
        if not eps_dic:
            eps_dic = {}
        # if show_id == MyEpisodes.SHOW_NOT_FOUND:
        #     raise Errors.
        data_parser = {'showid': show_id}
        response = requests.post(MyEpisodes.EPISODES_AJAX_URL, data_parser)

        soup = BeautifulSoup(response.content, 'lxml')
        tags = soup.find_all('tr')
        for id, tag in enumerate(tags[2:]):
            txt = tag.text
            if tag.attrs['class'][0] == 'header':
                continue
            items = txt.split("\n")
            if len(items) < 5:
                continue
            release_date = str(items[1])
            ep_str = str(items[3].lower())
            season_num = str(ep_str[1:3])
            episode_num = str(ep_str[4:])
            episode_name = items[4]
            if ":" in  episode_name:
                episode_name = episode_name.split(": ")[1]

            if season_num not in eps_dic:
                eps_dic[season_num] = {}

            if episode_num not in eps_dic[season_num]:
                eps_dic[season_num][episode_num] = Episode(series_name,
                                                                season_num,
                                                                episode_num,
                                                                episode_name,
                                                                release_date)
        return eps_dic

    @staticmethod
    def get_show_id(series_name):

        show_name = series_name.lower()
        firstLetter = show_name[0]
        firstWord = show_name.split()[0]
        if firstWord == 'the':
            firstLetter = show_name[4]
        url = MyEpisodes.SHOW_ID_URL + firstLetter.capitalize()

        try:
            data = urllib2.urlopen(url).read().lower()
        except Exception as ex:
            raise Errors.WebSiteUnresponsive(url)


        index = data.find('/' + show_name)
        last_index = data.find('\"', index)
        show = data[index + 1:last_index]
        counter = 5
        while show != show_name:
            index = data.find('/' + show_name, last_index)
            last_index = data.find('\"', index)
            show = data[index + 1:last_index]
            if counter == 0:
                raise Errors.BadShowId(show_name)
            counter -= 1
        show_details = data[index - 20:index]
        show_id = show_details[show_details.find('epsbyshow/') + 10:]

        MyEpisodes.show_id_dic[series_name] = show_id
        return show_id


    # @staticmethod
    # def get_lst_of_shows_in_specific_date(date):
    #     pass
    #     str = 'longnumber\">'
    #     # data = urllib2.urlopen("https://www.myepisodes.com/epsbydate/" + date).read().lower()
    #     date_str = date.to_string()
    #     url = "https://www.myepisodes.com/epsbydate/" + date
        # # req = read_webSite(url)
        # if req is None:
        #     return False
        # data = req.text.lower()
        # for show, id in MY_SHOWS.items():
        #     if id == -1:  # if show was not found
        #         continue
        #     show_index = data.find(show)
        #     while show_index != -1:
        #         id_index_start = data.find("/", show_index - 10) + 1
        #         id_index_end = data.find("/", id_index_start + 1)
        #         show_id_on_site = data[id_index_start:id_index_end]
        #         episode_number = data.find(str, id_index_start)
        #         showName = show + ' ' + data[episode_number + 12:episode_number + 18]
        #         if showName[-6] != 's':
        #             break
        #         if show_id_on_site == id:
        #             EPS_TO_DOWNLOAD_SINCE_UPDATE[showName.lower()] = date
        #         show_index = data.find(show, show_index + len(show) + 10)


    @staticmethod
    def get_all_shows_by_letter(letter):
        url = ""
        try:
            all_shows_lst = []
            if letter != '#':
                print letter
            url = MyEpisodes.SHOW_ID_URL + letter.capitalize()
            data = urllib2.urlopen(url).read().lower()
            parse_str = "</a></td>"
            shows_lst_data = data.split(parse_str)

            for item in shows_lst_data[:-1]:
                show = item[item.rfind("\">") + 2:]
                all_shows_lst.append(show)

            return all_shows_lst

        except Exception as ex:
            ex.args.__add__(url)
            raise ex



