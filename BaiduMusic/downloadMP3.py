#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2013年10月3日

@author: kjw
'''
import urllib2
from bs4 import BeautifulSoup
import re
import os
import sys
from KuWo import Top100
from KuWo.Top100 import fetch, billBoardList

SEARCH_URL = "http://music.baidu.com/search?key="
DOWNLOAD_DIR = "/home/alchemist000/Music/"

def searchSong(song, singer = None):
    name = singer + '_' + song + '.mp3'
    #print name
    if name in os.listdir(DOWNLOAD_DIR):
        print '已拥有' + name
        return        
    
    url = SEARCH_URL + song + singer
    url = url.replace(' ','%20')    #空格会出问题
    doc = urllib2.urlopen(url).read()
    #print doc
    soup = BeautifulSoup(doc)
    #print soup.find('a',{'href':re.compile("/song/[0-9]*")})['href']
    url = "http://music.baidu.com" + soup.find('a',{'href':re.compile("/song/[0-9]*")})['href']
    #print url
    doc = urllib2.urlopen(url).read()
    #print doc
    soup = BeautifulSoup(doc)
    return soup.find('a',{'download_url':re.compile('http:.*')})['download_url']

def downloadSong(url, singer, song):
    name = singer + '_' + song
    f = urllib2.urlopen(url)
    
    with open(DOWNLOAD_DIR + name + '.mp3', "wb") as code:
        code.write(f.read())

urlList = [
           ]

if __name__ == '__main__':
    boardLen = len(billBoardList) - 1
    index = input("请输入0~" + str(boardLen) + ": ")
    if index not in range(0,len(billBoardList)):
        print "超出范围"
        exit(1)
    url = billBoardList[index][1]
    print '您选择:',billBoardList[index][0]
    
    dict = fetch(url)
    length = len(dict)
    i = 0
    for song in dict:
        print "正在下载第" + str(i) + "首歌：" + dict[song] + "的"+ song
        try:
            url = searchSong(singer = dict[song], song = song)
            if url:
                downloadSong(url, singer = dict[song], song = song)
        except:
            log = open('error.log','w+')
            log.write('下载出错：' + dict[song] + "的"+ song)
            log.write(str(sys.exc_info()[0]))
            log.write(str(sys.exc_info()[1]))
            log.close()
        i += 1
    print "下载完成"