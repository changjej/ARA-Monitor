#-*-coding:utf-8-*-
import pyapns
import xmlrpclib
from gcm import GCM
from logger import *
from os import path
from etc.settings import RESOURCES_DIRECTORY 
IPHONE_PUSH_LENGTH = 40
class PyapnsWrapper(object):
 
    def __init__(self, host, app_id, apns_certificate_file, mode='sandbox'):
        self.app_id = app_id
        pyapns.configure({'HOST': host})
        pyapns.provision(app_id,
                         open(path.join(RESOURCES_DIRECTORY,apns_certificate_file)).read(),
                         mode)
 
    def notify(self, token, message,boardname,article_id):
        try:
            if len(message) > IPHONE_PUSH_LENGTH :
                message = message[:IPHONE_PUSH_LENGTH]+"..."
            pyapns.notify(self.app_id,
                          token,
                          {'aps':{'alert': message,'sound':'default','badge':1},'data':{'boardname':boardname,'article_id':article_id}})

        except xmlrpclib.Fault, e:
            log_error(str(e))


class PygcmWrapper(object):
    def __init__(self,api_key) :
        self.api_key = api_key 

    def notify(self,reg_id,title,message,boardname,article_id) :
        try :
            gcm =  GCM(self.api_key) 
            push_title = "["+boardname+"]"+title
            if len(message) > 1024 :
                message = message[:1024]+'...'
            data = {"title":push_title.encode('utf-8'),"message":message.encode('utf-8'),'article_id':article_id,'boardname':boardname}
            response = gcm.plaintext_request(registration_id=reg_id,data=data)
            log(" GCM Response : %s"%response)
        except Exception,e :
            log_error(str(e))
