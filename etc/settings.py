#-*-coding:utf-8-*-

#
# 1. Program Global Setting 
#
DEBUG = True
RESOURCES_DIRECTORY = 'resources'
receiver_file = 'receivers'

#
# 2. Register Server Related Settings
#
register_server_port = 15000

#
# 3. Crawler Settings
#
period = 120.0
#boardnames = ['ToSysop','Wanted','BuySell','Notice','Garbages','Food','Love','Infoworld','FunLife','Lostfound','QandA','Hobby','Siggame']
index_file_name = 'index'

#
# 4. Email Settings
#
#ara_id = 'example'
gmail_user = "changjej@gmail.com"
#ARA_PASSWORD = ''
GMAIL_PASSWORD = ''

# 
# 5. Push Settings
#
# 5.1 APNS
#APNS_pem_name = 'apns.pem'

# 5.2 GCM
#GCM_API_KEY = 'exampleKEY'

#
# 6. Log Settings
#
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y/%m/%d %H:%M:%S"
LOG_SIZE = 100*1024*1024 
LOG_DIRECTORY='logs'
log_file_name = 'ara_crawling.log'
web_log = 'web.log'

#
# 7. Extra Settings
# settings_local file should have GMAIL_PASSWORD and ARA_PASSWORD
#
try:
    from settings_local import *
except:
    pass
