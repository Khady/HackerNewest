#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import time
import sqlite3
import datetime
import jinja2
import uuid
from bs4 import BeautifulSoup

DATABASE = "hn.db"
FLUX = "flux.xml"

def date_internet(date):
    d = date.strftime('%Y-%m-%dT%H:%M:%S%z')
    return d[:-2] + d[-2:] + 'Z'

def connect_db():
    return sqlite3.connect(DATABASE)

def init_db(s = 'schema.sql'):
    schema = open(s)
    db = connect_db()
    db.cursor().executescript(schema.read())
    db.commit()
    db.close()
    schema.close()

class HackerNewest:
    """generate a list of links from the page newest on hackernews
    """
    def __init__(self):
        self.url = 'http://news.ycombinator.com/newest'
        self.surl = 'http://news.ycombinator.com'
        self.page = ""
        self.links = []

    def get_page(self):
        """fetch page
        """
        try:
            self.page = urllib.request.urlopen(self.url).read()
        except urllib.error.URLError:
            self.page = ""

    def get_links(self):
        """get all the news links in the page
        """
        soup = BeautifulSoup(self.page)
        vote = False
        infos = []
        for link in soup.find_all('a'):
            l = link['href']
            if l.startswith('vote'):
                vote = True
            elif vote == True:
                infos = [jinja2.Markup.escape(link.string), jinja2.Markup.escape(l), date_internet(datetime.datetime.now())]
                time.sleep(1)
                vote = False
            elif l.startswith('item'):
                infos.append("%s/%s" % (self.surl, l))
                infos.append(uuid.uuid3(uuid.NAMESPACE_DNS, infos[1]))
                self.links.append(infos)
        return self.links

class ArchiveLinks:
    """archive every links into a sqlite database
    """
    def __init__(self):
        pass

class GenAtom:
    """generate an atom feed from an array with : [title, link, date, summary, id]
    This class use templates with jinja2. This is not the best solution but it works
    """
    def __init__(self):
        self.rss = ''
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader("."))

    def set_items(self, links):
        self.rss = self.env.get_template("feedtemplate.xml").render(date=date_internet(datetime.datetime.utcnow()),
                                                                    items=links)

    def get_flux(self):
        return self.rss

if __name__ == '__main__':
    """Get the links from hackernews and generate an atom feed every minutes
    """
    hn = HackerNewest()
    gen = GenAtom()
    while True:
        hn.get_page()
        links = hn.get_links()
        gen.set_items(links)
        rss = gen.get_flux()
        f = open(FLUX, 'w')
        print (rss)
        f.write(rss)
        f.close()
        time.sleep(30)
