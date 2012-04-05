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
SITE = "http://docs.khady.info"

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
                infos = [jinja2.Markup.escape(link.string),
                         jinja2.Markup.escape(l.strip()),
                         date_internet(datetime.datetime.now())]
                time.sleep(1)
                vote = 2
            elif l.startswith('item') and vote == 2:
                infos.append("%s/%s" % (self.surl, l))
                infos.append(uuid.uuid3(uuid.NAMESPACE_DNS, infos[1]))
                links.append(infos)
                vote = 0
        return links

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
                                                                    items=links,
                                                                    site="%s/%s" % (SITE, FLUX),
                                                                    uid=uuid.uuid3(uuid.NAMESPACE_DNS, SITE))

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
        f = open("%s/%s" % ("/home/sites/docs.khady.info/htdocs", FLUX), 'w')
        print (rss)
        f.write(rss)
        f.close()
        time.sleep(30)
