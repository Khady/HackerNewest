#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import urllib.request
from modules.internet import date_internet
from bs4 import BeautifulSoup
from uuid import uuid3, NAMESPACE_DNS
from jinja2 import Markup
from datetime import datetime

class HackerNewest:
    """generate a list of links from the page newest on hackernews
    """
    def __init__(self, url, surl):
        self.url = url
        self.surl = surl
        self.page = ""

    def get_page(self):
        """fetch page
        """
        try:
            self.page = urllib.request.urlopen(self.url).read()
        except:
            self.page = ""

    def get_links(self):
        """get all the news links in the page
        """
        soup = BeautifulSoup(self.page)
        vote = 0
        infos = []
        links = []
        for link in soup.find_all('a'):
            l = link['href']
            if l.startswith('vote'):
                vote = 1
            elif vote == 1:
                if l.startswith("item"):
                    l = "%s/%s" % (self.surl, l)
                infos = [Markup.escape(link.string),
                         Markup.escape(l.strip()),
                         date_internet(datetime.now())]
                time.sleep(1)
                vote = 2
            elif l.startswith('item') and vote == 2:
                infos.append("%s/%s" % (self.surl, l))
                infos.append(uuid3(NAMESPACE_DNS, infos[1]))
                links.append(infos)
                vote = 0
        return links
