# -*- coding: utf-8 -*-
import os
import urllib.request
from PIL import Image
import requests
from bs4 import BeautifulSoup


class Img():
    def __init__(self, ss_url, imname):
        self.s_url = str(ss_url)
        self.gi_url = 'https://namu.wiki/w/'
        self.urll =self.gi_url + imname
        self.savename = './image/' + self.s_url + ".gif"
        self.winkimg = './image/wink.gif'

    def getimg(self):
        text = requests.get(self.urll).text
        soup = BeautifulSoup(text, 'html.parser')
        imagelist = soup.find("div", class_="wiki-table-wrap table-right")
        imlist = imagelist.find("img", class_="wiki-image")

        ilist = imlist.get("data-src")
        imsrc = str(ilist)
        rsrc = "https:" + imsrc

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(rsrc, self.savename)

        y1 = Image.open(self.savename)
        y1size = 300, 320
        rey1 = y1.resize(y1size)
        rey1.save(self.savename)
