#!/usr/bin/env python
#-*-coding:utf-8-*-
import sys,os
import urllib,urllib2,cookielib
from bs4 import BeautifulSoup
from os import remove
from shutil import move
import os, smtplib
from email.mime.text import MIMEText
from email import Encoders
import threading
from etc.settings import *
from logger import *
from setproctitle import setproctitle

def loads(receiver_list_file) :
    '''
    @param receiver_list_file : file that contains receivers in json format
    @type receiver_list_file : strip
    @rtype : lists
    @return : lists of the receivers 
    '''
    f = open(receiver_list_file,'r')
    receivers = [] 
    for line in f:
        if line.strip()[0]=="#" :
            continue
        elif line.strip()=="" :
            continue
        receivers.append(line.strip())
    f.close()
    return receivers

def login() :
    '''
    @rtype : opener
    @return : opener which has interpark ticket infos
    '''
    url = "http://ticket.interpark.com/webzine/paper/TPNoticeList_iFrame.asp?bbsno=0&pageno=0&stext=&KindOfGoods=&Genre=&sort="
    jar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
    return opener

def read_board(opener) :
    '''
    read the article lists of board with boardname 

    @type opener : urllib2.opener
    @param opener : opner with login cookie 
    @rtype : list 
    @return : list of articles_id 
    '''
    read_url = "http://ticket.interpark.com/webzine/paper/TPNoticeList_iFrame.asp?bbsno=0&pageno=0&stext=&KindOfGoods=&Genre=&sort="
    read_handler = opener.open(read_url)
    read_resp = unicode(read_handler.read(), "euc-kr").encode("utf-8")

    soup = BeautifulSoup(read_resp)
    articles = soup.findAll('a',attrs={'target':'_top'})
    article_links = map(lambda x:'http://ticket.interpark.com/webzine/paper/'+x.attrs['href'],articles)
    article_ids = []
    for i in article_links:
        split_start_index = i.find('&no=')
        split_end_index = i.find('&',split_start_index+1)
        seq = i[split_start_index+4:split_end_index]
        article_ids.append(seq)
    article_titles = map(lambda x:x.text,articles)
    return (article_ids,article_titles,article_links)

def compare_index(articles) :
    '''
    @type articles : list
    @param articles : article ids
    '''
    index_file = open(path.join(RESOURCES_DIRECTORY,index_file_name),'r')
    last_index = int(index_file.readline().strip())
    index_file.close()
    max_id = int(articles[0])
    for i in articles:
        if max_id < int(i) :
            max_id = int(i)
    log("max id : %d ,last index: %d"%(max_id,last_index))
    if last_index >= max_id:
        return (0,0)
    else :
        return (last_index,max_id)

def update_file(new_id) :
    '''
    @type new_id : str
    @param new_id : new max id of board articles
    @type boardname : str   
    @param boardname : the board name 
    '''
    fo = open(path.join(RESOURCES_DIRECTORY,index_file_name)+'.tmp','w')
    fi = open(path.join(RESOURCES_DIRECTORY,index_file_name),'r')
    fo.write(str(new_id))

    fo.close()
    fi.close()
    remove(path.join(RESOURCES_DIRECTORY,index_file_name))
    move(path.join(RESOURCES_DIRECTORY,index_file_name)+'.tmp',path.join(RESOURCES_DIRECTORY,index_file_name))

 
def send_gmail(to, subject, text):
    msg=MIMEText(text)
    msg['From']="interpark_crawler"
    msg['To']=to
    msg['Subject']="[INTERPARK_MONITOR] "+subject
    msg = msg.as_string()

    mailServer=smtplib.SMTP("smtp.gmail.com",587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user,GMAIL_PASSWORD)
    mailServer.sendmail(gmail_user, to, msg)
    mailServer.close()
    log( "Mail sent : %s"%to )

def find_index(l,articleid) :
    domain = range(len(l))
    domain.reverse()
    for i in domain : 
        if int(l[i]) >=int(articleid) :
            return i

def crawl_wrap() :
    log ("Start Crawl")
    threading.Timer(period, crawl_wrap).start()
    crawl()
    log ("End Crawl")

def crawl() :
    log ("start")
    receivers = loads(path.join(RESOURCES_DIRECTORY,receiver_file))
    log (receivers)
    log( "RECEIVERS : ")
    for i in receivers :
        log (" email : %s"%(i))

    opener = login()
    article_ids,article_titles,article_links = read_board(opener)
    last_index,max_id = compare_index(article_ids)
    if last_index != 0 :
        index = find_index(article_ids,last_index)
        if DEBUG: print "index : %s"%index
        if DEBUG: print "article_ids : %s"%article_ids
        update_file(max_id)
        l = range(0,index)
        l.reverse()
        for i in l:
            log("Title: %s"%article_titles[i])
            for receiver in receivers:
                send_gmail(receiver,article_titles[i],article_links[i])

def main():
    try: 
        pid = os.fork()
        if pid > 0: 
            sys.exit(0)
    except OSError,e:
        log_error("fork failed")
        sys.exit(1)

    setproctitle("interpark_crawler")
    crawl_wrap()
    register.run()

