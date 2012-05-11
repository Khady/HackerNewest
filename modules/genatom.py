#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from jinja2 import Markup, Environment, FileSystemLoader
from modules.internet import date_internet
from uuid import uuid3, NAMESPACE_DNS

class GenAtom:
    """generate an atom feed from an array with : [title, link, date, summary, id]
    This class use templates with. This is not the best solution but it works.
    """
    def __init__(self, site, flux):
        self.env = Environment(loader=FileSystemLoader("."))
        self.site = site
        self.flux = flux

    def set_items(self, links):
        self.links = links

    def get_flux(self):
        return self.env.get_template("feedtemplate.xml").render(date=date_internet(datetime.utcnow()),
                                                                    items=self.links,
                                                                    site="%s/%s" % (self.site, self.flux),
                                                                    uid=uuid3(NAMESPACE_DNS, self.site))
