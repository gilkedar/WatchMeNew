
from time import sleep
import os
import Errors

import requests
import Config
import threading
from bs4 import BeautifulSoup

class Website:

    HDR = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    def __init__(self,url):

        self.url = url
        self.ip = self.get_ip()
        self.is_alive = False
        # self.lock = threading.Lock()

        # self.check_if_alive()

    def get_ip(self):
        pass

    def read_webSite(self,url=None, timeout=Config.WEBSITES_TIMEOUT_IN_SECONDS):

        try:
            if not url:
                url = self.url
            # else:
            #     self.check_if_alive(url)
            # start = time.time()
            sleep(0.1)

            req = requests.get(url, headers=self.HDR, verify=os.path.join('cacert.pem'), timeout=timeout)

            if req.status_code == 200:
                 return req.text

            if req.status_code == 404:
                raise Errors.WebSiteDead
            if req.status_code == 409:
                return Errors.WebSiteUnresponsive


            # return req

        except Exception as ex:
            raise ex

    def check_if_alive(self,url=None):
       
        if not url:
            url = self.url
       
        r = requests.head(url)
        if not r.status_code == 200:
            raise Errors.WebSiteDead(self)
