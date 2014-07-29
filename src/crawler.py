#!venv/bin/python   
#-*-coding:utf-8-*-
import sys
import urllib,urllib2,cookielib
from bs4 import BeautifulSoup
from os import remove
from shutil import move
import os, smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from email.header import Header
import threading
from pusher import PyapnsWrapper,PygcmWrapper
from etc.settings import *
from logger import *
import json
import register
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
        receivers.append(json.loads(line))
    f.close()    
    return receivers

def login() :
    '''
    @rtype : opener
    @return : opener which has cookie of account 
    '''
    url = "http://ara.kaist.ac.kr/account/login/"
    form_data = {'username' : ara_id, 'password' : ARA_PASSWORD}
    jar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
    form_data = urllib.urlencode(form_data)
    login_handler = opener.open(url,form_data)
    login_response = login_handler.read()
    if 'failed' in login_response :
        log_error("Login Failed")
        log_error(login_response)
    else :
        log( "Login Success" )
    return opener

def get_article_body(boardname,articleid,opener) :
    read_url = "http://ara.kaist.ac.kr/board/%s/%s/"%(boardname,articleid)
    read_handler = opener.open(read_url)
    read_resp = read_handler.read()
    soup = BeautifulSoup(read_resp)
    article_body = soup.findAll('div',attrs={'class':'article '})
    article_body = article_body[0].text
    if DEBUG: print article_body
    log("Body : %s"%article_body)
    return article_body

def read_board(boardname,opener) :
    '''
    read the article lists of board with boardname 

    @type boardname : str
    @param boardname : the name of board
    @type opener : urllib2.opener
    @param opener : opner with login cookie 
    @rtype : list 
    @return : list of articles_id 
    '''
    read_url = "http://ara.kaist.ac.kr/board/%s"%boardname
    read_handler = opener.open(read_url)
    read_resp = read_handler.read()

    soup = BeautifulSoup(read_resp)
    article_ids = soup.findAll('td',attrs={'class':'articleid hidden'})
    article_titles = soup.findAll('td',attrs={'class':'title'}) 

    article_ids = map(lambda x: int(x['rel']),article_ids)
    article_titles = map(lambda x:x.text,article_titles)
    articles = []
    while len(article_ids) > len(article_titles) :
        #Remove 공지사항 
        article_ids.pop(0)
    return (article_ids,article_titles)

def compare_index(articles,boardname) :
    '''
    @type articles : list
    @param articles : article ids
    '''
    index_file = open(path.join(RESOURCES_DIRECTORY,index_file_name),'r')
    last_index = 0
    lines = index_file.readlines()
    for line in lines:
        if boardname in line :
            last_index = int(line.split(",")[0])
            break
    index_file.close()
    max_id = int(articles[0])
    for i in articles:
        if max_id < int(i) :
            max_id = int(i)
    log("(%s) max id : %d ,last index: %d"%(boardname,max_id,last_index))
    if last_index >= max_id:
        return (0,0)
    else :
        return (last_index,max_id)

def update_file(new_id,boardname) :
    '''
    @type new_id : str
    @param new_id : new max id of board articles
    @type boardname : str   
    @param boardname : the board name 
    '''
    fo = open(path.join(RESOURCES_DIRECTORY,index_file_name)+'.tmp','w')
    fi = open(path.join(RESOURCES_DIRECTORY,index_file_name),'r')
    for line in fi.readlines() :
        if boardname in line : 
            fo.write("%s,%s\n"%(new_id,boardname))
        else :
            fo.write(line)

    fo.close()
    fi.close()
    remove(path.join(RESOURCES_DIRECTORY,index_file_name))
    move(path.join(RESOURCES_DIRECTORY,index_file_name)+'.tmp',path.join(RESOURCES_DIRECTORY,index_file_name))

 
def send_gmail(to, subject, text,boardname):
    msg=MIMEMultipart()
    msg['From']="ara_crawler"
    msg['To']=to
    msg['Subject']=Header(s="[ARA_MONITOR][%s]%s"%(boardname,subject),charset="utf-8")
    msg.attach(MIMEText(text,_charset="utf-8"))

    mailServer=smtplib.SMTP("smtp.gmail.com",587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user,GMAIL_PASSWORD)
    mailServer.sendmail(gmail_user, to, msg.as_string())
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
    try:
        receivers = loads(path.join(RESOURCES_DIRECTORY,receiver_file))
        log( "RECEIVERS : ")
        for i in receivers :
            log (" email : %s , device : %s , token : %s"%(i[0],i[4],i[5]))

        ios_pusher = PyapnsWrapper("http://localhost:7077","aramonitor",APNS_pem_name)
        and_pusher = PygcmWrapper(GCM_API_KEY)
        opener = login()
        for boardname in boardnames:
            article_ids,article_titles =read_board(boardname,opener)
            last_index,max_id = compare_index(article_ids,boardname)
            if last_index != 0 :
                index = find_index(article_ids,last_index)
                if DEBUG: print "index : %s"%index
                if DEBUG: print "article_ids : %s"%article_ids
                update_file(max_id,boardname)
                l = range(0,index)
                l.reverse()
                for i in l:
                    log("Title: %s"%article_titles[i])
                    text = get_article_body(boardname,article_ids[i],opener)
                    for user,boards,email_enable,push,device,token in receivers:
                        if boardname in boards:
                            if email_enable:
                                send_gmail(user,article_titles[i],text,boardname)
                            if push:
                                log("Push sent : %s"%user)
                                if device =='android':
                                    and_pusher.notify(token,article_titles[i],text,boardname,article_ids[i])
                                elif device == 'ios':
                                    ios_pusher.notify(token,"[%s]%s"%(boardname,article_titles[i]),boardname,article_ids[i])
    except Exception,e:
        log_error( "Exception Occured : %s"%e)

def main():
    try: 
        pid = os.fork()
        if pid > 0: 
            sys.exit(0)
    except OSError,e:
        log_error("fork failed")
        sys.exit(1)
    
    setproctitle("aracrawler")
    os.system('twistd -r epoll web --logfile=%s --class=pyapns.server.APNSServer --port=7077'%(path.join(LOG_DIRECTORY,'twistd.log')))
    crawl_wrap()
    register.run()

