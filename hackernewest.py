#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import time
import sqlite3
from datetime import datetime
from jinja2 import Markup, Environment, FileSystemLoader
from uuid import uuid3, NAMESPACE_DNS
from bs4 import BeautifulSoup
from os import path

DATABASE = "hn.db"
SITE = "http://sample.tld"
FLUX = "flux.xml"
FLUX_DEST_PATH = "."

def date_internet(date):
    d = date.strftime('%Y-%m-%dT%H:%M:%S%z')
    return d[:-2] + d[-2:] + 'Z'

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

class ArchiveLinks:
    """archive every links into a sqlite database
    """
    def __init__(self, create_base = False, s = 'schema.sql'):
        if create_base is True and not path.isfile(DATABASE):
            self.init_db(s)
        pass

    def connect_db(self):
        return sqlite3.connect(DATABASE)

    def init_db(self, s):
        schema = open(s)
        db = self.connect_db()
        db.cursor().executescript(schema.read())
        db.commit()
        db.close()
        schema.close()

    def archive(self, link):
        db = self.connect_db()
        data = link[0:4]
        data.append(str(link[4]))
        db.execute('INSERT INTO archive (title, link, date, summary, postid) values (?, ?, ?, ?, ?)',
                   data)
        db.commit()
        db.close()

    def archive_all(self, links):
        db = self.connect_db()
        for link in links:
            if db.execute('SELECT postid FROM archive WHERE postid = ?', [str(link[4])]).fetchall():
                break
            data = link[0:4]
            data.append(str(link[4]))
            db.execute('INSERT INTO archive (title, link, date, summary, postid) values (?, ?, ?, ?, ?)',
                       data)
            db.commit()
        db.close()


class GenAtom:
    """generate an atom feed from an array with : [title, link, date, summary, id]
    This class use templates with. This is not the best solution but it works.
    """
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader("."))

    def set_items(self, links):
        self.links = links

    def get_flux(self):
        return self.env.get_template("feedtemplate.xml").render(date=date_internet(datetime.utcnow()),
                                                                    items=self.links,
                                                                    site="%s/%s" % (SITE, FLUX),
                                                                    uid=uuid3(NAMESPACE_DNS, SITE))

def run():
    """Get the links from hackernews and generate an atom feed every minutes
    """
    hn = HackerNewest()
    gen = GenAtom()
    archives = ArchiveLinks(True)
    while True:
        hn.get_page()
        links = hn.get_links()
        archives.archive_all(links)
        gen.set_items(links)
        rss = gen.get_flux()
        f = open("%s/%s" % (FLUX_DEST_PATH, FLUX), 'w')
        f.write(rss)
        f.close()
        print (rss)
        time.sleep(30)

if __name__ == '__main__':
    run()
