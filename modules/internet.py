#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def date_internet(date):
    d = date.strftime('%Y-%m-%dT%H:%M:%S%z')
    return d[:-2] + d[-2:] + 'Z'
