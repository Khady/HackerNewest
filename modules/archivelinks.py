#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from os import path

class ArchiveLinks:
    """archive every links into a sqlite database
    """
    def __init__(self, database, create_base = False, s = 'schema.sql'):
        self.database = database
        if create_base is True and not path.isfile(self.database):
            self.init_db(s)

    def connect_db(self):
        return sqlite3.connect(self.database)

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
