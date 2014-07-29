from settings import *
from pusher import *
pusher = PyapnsWrapper("http://localhost:7077","aramonitor",APNS_pem_name)
pusher.notify('7e94993b02ddd866147539dda32965e357b570df1c2f07ec5eff5ab626fa82aa',"Test","Test",2014012)

