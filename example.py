import PaperWatchDog as pwd 
from mywebhook import *  

dog = pwd.WatchDog(WEBHOOK_URL)

dog.run(pwd.watch_list)
