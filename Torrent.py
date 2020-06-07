
from File import File
import Config
import os
import subprocess
import Errors

class Torrent:

    RELEASE_NAMES = ['dimension', 'fleet', 'immerse', 'avs', 'killers', 'deejayahmed', 'msd',
                     'megusta', 'psa', 'wifi', 'yify', 'fum', 'lol', 'turbo', 'publichd', 'subs',
                     'avs', 'shaanig', 'deflate','rmteam', 'skgtv', 'batv', 'belex', 'demand', 'nate']

    QUALITY_TYPES = ['720p','1080p','xvid','divx']

    def __init__(self,item_name,item_type,torrent_name,num_of_seeders, magnet_link):
        self.torrent_name = torrent_name
        self.item_name = item_name
        self.item_type = item_type
        self.num_of_seeders = num_of_seeders
        self.magnet_link = magnet_link

        self.release = self.get_release()
        self.quality = self.get_quality()

    def get_release(self):

        fileName = self.torrent_name
        dash_idx = fileName.rfind('-')
        lastPart_idx = fileName.rfind('.')
        if lastPart_idx < 0:
            lastPart_idx = fileName.rfind("[")
        if lastPart_idx < 0:
            lastPart_idx = fileName.rfind("-")
        lastPart = fileName[lastPart_idx + 1:]
        lastPart = lastPart.strip(' ')
        lastPart = lastPart.strip(']')
        # if lastPart[-1] == "]":

        try:
            if '-' in fileName or lastPart in self.RELEASE_NAMES:
                release = fileName[dash_idx + 1:]
                if lastPart in self.RELEASE_NAMES:
                    return lastPart

                if release == "":
                    return ""

                if release[0] == '.':
                    release = release[1:]
                if release[0] == ' ':
                    release = release[1:]
                if release[-1] == ' ':
                    release = release[:-1]
                if '[' in release:
                    release = release[:release.find('[')]
                if '.' in release:
                    release = release[:release.find('.')]
                if ' ' in release:
                    release = release[:release.find(' ')]
                if '-hi' in release:
                    release = release[:release.find('-hi')]
                if release != 'dl':
                    # if release not in RELEASE_NAMES:
                    #     for possible_release in RELEASE_NAMES:
                    #         if possible_release in fileName:
                    #             return possible_release
                    return release.lower()
            return ''

        except Exception as ex:
            # RUNTIME_ERRORS.append("Could not get release for '" + fileName )
            return ''

    def get_quality(self):
        for quality in self.QUALITY_TYPES:
            if quality in self.torrent_name:
                return quality
        else:
            return "" #default


    def download(self):
        #
        # if SHUTDOWN_OUTPUT_SCREEN:
        #     return
        try:
            if os.name == 'nt':  # Windows
                os.startfile(self.magnet_link)
            elif os.uname()[0] == 'Linux':  # Linux
                subprocess.call(["xdg-open", self.magnet_link])
            else:  # Don't know what you are, hope the OS can open a magnet URL!
                os.startfile(self.magnet_link)

        except Exception as ex:
            raise Errors.TorrentMagnetError(self)

    def check_if_valid(self):

        ok = True
        words = self.item_name.split(' ')
        words = [word.strip(".") for word in words]  # shows like mr. robot
        torrentWords = self.torrent_name.split('.')

        if len(torrentWords) < 4:
            torrentWords = self.torrent_name.split(' ')

        if words[0] != torrentWords[0]:
            if "hbo" not in torrentWords[0]:
                return False

        # if words[1] != torrentWords[1]:   # too strict for now
        #     if not torrentWords[-2:].isalnum():
        #         return False

        for word in words:
            if '(' in word:
                continue
            # if '.' in word:
            #     word = word.strip('.')
            if word == 'season':
                seasonNum = ''
                if "season" == words[-1]:
                    seasonNum = words[-2]
                    if seasonNum + " " in self.torrent_name:
                        continue
                    elif seasonNum + "." in self.torrent_name:
                        continue
                else:
                    seasonNum = self.torrent_name[self.torrent_name.find("season") + 7:]
                    if "season" in self.item_name:
                        if seasonNum in self.item_name[self.item_name.find("season") + 7:self.item_name.find("season") + 9]:
                            break
                    if len(seasonNum) == 1:
                        seasonNum = "0" + seasonNum
                    if "s" + seasonNum in self.item_name:
                        if seasonNum in self.item_name[self.item_name.find("s" + seasonNum): self.item_name.find("s" + seasonNum) + 6]:
                            break
                    else:
                        return False

            if word not in self.item_name:
                ok = False
                break

        return ok

        # elif '720p' not in self.item_name and Config.ONLY_HD_QUALITY_FLAG:  # and item != 'sub':
        #     if '1080p' not in self.item_name and Config.ONLY_HD_QUALITY_FLAG:
        #         return False
        #     else:
        #         return True
        # else:
        #     return True
