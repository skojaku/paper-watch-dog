import PaperWatchDog as pwd 

WEBHOOK_URL = "add your web hook url"

dog = pwd.WatchDog(WEBHOOK_URL)

dog.run(pwd.watch_list)
