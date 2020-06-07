from bs4 import BeautifulSoup
import requests
import lxml
from lxml import html

from Website import Website


class IMDB_Class:

    IMDB_URL = 'http://www.imdb.com/'


    @staticmethod
    def get_imdb_url(search_name):

        url = IMDB_Class.IMDB_URL + "find?ref_=nv_sr_fn&q=" + '+'.join(search_name.lower().split()) + '&s=all'

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        next_page = soup.find('td', 'result_text')
        tag = next_page.find_all('a',href=True)
        href = tag[0].attrs['href']

        show_link = IMDB_Class.IMDB_URL + href
        return show_link

    @staticmethod
    def get_imdb_rating(item_url):

        imdb_site = Website(item_url)

        text = imdb_site.read_webSite()
        soup = BeautifulSoup(text,"html.parser")
        for span in soup.findAll('span'):
            if span.has_key('itemprop') and span['itemprop'] == 'ratingValue':
                rating = span.contents[0]
                return float(rating)

        return None


