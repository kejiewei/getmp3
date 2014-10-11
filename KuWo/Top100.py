#!/usr/local/bin/python2.7
# encoding: utf-8
'''
Created on 2013年10月3日

@author: kjw
'''
from mechanize import Browser
from bs4 import BeautifulSoup
import urllib2
import re

billBoardList = []


def getTitle(tag):  
    return re.split('[<>]',str(tag))[2]

def getTitleList(tagList):  #没用了
    titleList = []
    for tag in tagList:
        #print tag
        titleList.append(getTitle(tag))
    return titleList

def twoListToDict(listA, listB):    #连接两个列表，为一个字典
    #print len(listA),len(listB)
    #if len(listA) != len(listB):
    #    return
    length = min(len(listA),len(listB))
    dict = {}
    for i in range(0, len(listA)):
        #print listA[i],listB[i]
        dict[listA[i]] = listB[i]
    return dict

def getAList(liList):   #获取网页上的所有歌曲链接a
    aList = []
    print 'liList:',len(liList)
    for li in liList:
        try:
            #print re.split('[<>]',str(li))
            #print li
            item = re.split('[<>]',str(li))[4]
            if item and item != '':
                aList.append(item);
        except:
            pass
    return aList

def fetch(LOGIN_URL = "http://yinyue.kuwo.cn/yy/billboard_%E7%BE%8E%E5%9B%BDThe+Billboard+Hot+100.htm#@"):
    doc = urllib2.urlopen(LOGIN_URL).read()
    #file_object = open('a.html', 'w')
    #file_object.writelines(doc)
    #file_object.close( )
    soup = BeautifulSoup(doc)
    songs = getAList(soup.findAll('li', {'class':'songName'}))
    singers = getAList(soup.findAll('li', {'class':'songer'}))
    #for song in songs:
    #    print song
    #print "--------------"
    #for singer in singers: 
    #    print singer
    return twoListToDict(songs, singers)

def getBillBoardList():
    doc = urllib2.urlopen("http://yinyue.kuwo.cn/yy/billboard_index.htm").read()
    soup = BeautifulSoup(doc)
    links = soup.findAll('a', {'href':re.compile('http://yinyue.kuwo.cn/billboard.*')})
    for link in links:
        #print link
        billBoardList.append((re.split('[<>]',str(link))[2],(re.search('http.+htm',str(link))).group(0)))
    #print billBoardList
    i = 0
    for board in billBoardList:
        print i, board[0], board[1]
        i += 1
    return billBoardList
    
getBillBoardList()
#print fetch()
#print fetch("http://yinyue.kuwo.cn/yy/billboard_%E4%B8%AD%E5%9B%BD%E5%A5%BD%E5%A3%B0%E9%9F%B3%E6%A6%9C.htm")
