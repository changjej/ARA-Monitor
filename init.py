#!venv/bin/python 

import os 

def init():
    os.system("virtualenv venv")
    os.system("venv/bin/pip install -r requirements.txt")

    if os.path.isfile("etc/settings_local.py"):
        print "already exist"
        return
    settings_local_file = open("etc/settings_local.py","w")

    gmail_password = raw_input("gmail password : ")
    settings_local_file.write('GMAIL_PASSWORD="%s"\n'%gmail_password)
    settings_local_file.close()

    os.system("chmod 600 "+"settings_local.py")

    touch("etc/receivers")

init()
