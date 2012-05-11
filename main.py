#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from modules.genatom import GenAtom
from modules.internet import date_internet
from modules.archivelinks import ArchiveLinks
from modules.hackernewest import HackerNewest

URL = 'http://news.ycombinator.com/newest'
SITE_URL = 'http://news.ycombinator.com'
DATABASE = "hn.db"
SITE = "http://sample.tld"
FLUX = "flux.xml"
FLUX_DEST_PATH = "."
ARCHIVE = True
FEED = True

def run():
    """Get the links from hackernews and generate an atom feed every minutes
    """
    hn = HackerNewest(URL, SITE_URL)
    gen = GenAtom(SITE, FLUX)
    archives = ArchiveLinks(DATABASE, True)
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
