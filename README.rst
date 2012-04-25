============
HackerNewest
============

HackerNewest is a python script to save all links from http://news.ycombinator.com/newest and generate an atom feed

Installation
============

Download
--------

  git clone https://github.com/Khady/HackerNewest.git

Requirements
------------

This script is in python 3.

For me it works with:

- Jinja2==2.6
- beautifulsoup4==4.0.2

Setup
=====

You may change the globals at the begining of the script

- DATABASE
- SITE
- FLUX
- FLUX_DEST_PATH

Running
=======

  ./hackernewest.py

TODO
====

- Split this file into modules
- Add an option to launch a daemon
- Use configuration for choose if you want to archive the links and generate the atom feed
