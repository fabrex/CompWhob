import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class WhobCorpusExtraction:


    def __init__(self, url_presidency):

        self.url_presidency = url_presidency


    def extract_h_ref_links(self):

        '''
        :return: list of h_ref links contained in the url presidency parameter
        '''

        r = requests.get(self.url_presidency)
        soup = BeautifulSoup(r.content, 'html.parser')
        re_href = re.findall(r"\.\./ws/index\.php\?pid=[0-9]+", str(soup))

        links = []
        for link in re_href:
            new_link = link.replace("..", "")
            links.append("http://www.presidency.ucsb.edu" + new_link)


        return links


    def extract_h_ref_content(self):

        '''
        :return: a list of strings, where the string is the content structure for every h_ref link. Every year content
        consists of the conference date, conference title and conference year.
        '''

        links = self.extract_h_ref_links()

        contents = []
        for link in links:
            l = requests.get(link)
            soup = BeautifulSoup(l.content)
            l.close()
            conf_title = soup.find_all("span", {"class": "ver10"})
            conf_speech = soup.find("span", {"class": "displaytext"})
            conf_dates = soup.find("span", {"class": "docdate"})
            conf_date = conf_dates.text
            format_conf_date = datetime.strptime(conf_date, "%B %d, %Y")
            string_format_conf_date = str(format_conf_date).replace(" 00:00:00", "")
            corpus_date = ('<div1 n="' + string_format_conf_date + '">')
            contents.append(corpus_date + '\n' + conf_title[2].text + conf_speech.text)

        return contents