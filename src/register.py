#-*-coding:utf-8-*-
import sys
from flask import Flask,request,render_template
import json
from etc.settings import DEBUG,receiver_file,register_server_port,web_log,LOG_DIRECTORY,RESOURCES_DIRECTORY
from threading import Lock 
from os import remove, devnull
from shutil import move
from logger import *

app=Flask(__name__)

web_log_file= open(path.join(LOG_DIRECTORY,web_log),'a')
sys.stderr = web_log_file 
sys.stdout = web_log_file
lock = Lock()

@app.route("/register",methods=["POST"])
def register() :
    lock.acquire()
    try :
        email = request.form['email']
        boards = json.loads(request.form['boards'])
        email_enabled = True if request.form['email_enabled']=="True" else False
        push_enabled= True if request.form['push_enabled'] =="True" else False
        device_type = request.form['device_type']
        push_token = request.form['push_token']
        update_file(email,json.dumps([email,boards,email_enabled,push_enabled,device_type,push_token]))
    finally:
        lock.release()

    return "OK"

@app.route("/",methods=["GET"])
def index() :
    f = open(path.join(RESOURCES_DIRECTORY,receiver_file),'r')
    l = f.readlines()
    l = map(lambda x: json.loads(x),l)
    for i in l:
        s = ''
        for j in i[1] :
            s+= str(j)+'\n'
        i[1] = s
    return render_template('index.html',receivers=l)

def update_file(email,new_info) :
    fo = open(path.join(RESOURCES_DIRECTORY,receiver_file)+'.tmp','w')
    fi = open(path.join(RESOURCES_DIRECTORY,receiver_file),'r')
    not_found = True
    for line in fi.readlines() :
        if email in line : 
            fo.write(new_info+'\n')
            not_found = False
            log("update User : %s, Info : %s"%(email,new_info))
        else :
            fo.write(line)
    if not_found :
        fo.write(new_info+'\n')
        log("new User : %s, Info : %s"%(email,new_info))
    fo.close()
    fi.close()
    remove(receiver_file)
    move(receiver_file+'.tmp',receiver_file)

def run():
    app.debug = DEBUG
    log("Flask Started. PORT : %s"%register_server_port)
    app.run(host='0.0.0.0',port=register_server_port)


