# Written by Sadamori Kojaku 
#
# References:
# https://qiita.com/TatsuyaMizuguchi17/items/35dd3dd1396864006031
#
from .Paper  import Paper
import os
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import feedparser 
import time
import slackweb
import datetime as dt

class WatchDog(): 

    def __init__(self, WEBHOOK_URL):
        """
        Initializer of the WatchDog class

        Parameters
        ----------
        WEBHOOK URL: the url for the target slack channel (string)
                     To get the url, see https://api.slack.com/messaging/webhooks 
        """
        self.WEBHOOK_URL = WEBHOOK_URL # Webhook url for the target slack channel 
        self.REGISTERED_URL = ".paper-watch-dog.log" # Intermediately file
    

    def run(self, watch_list, verbose = True):
        """
        Check the RSS and send the update to your slack channel.

        Parameters
        ----------
        watch_list: list of rss to be watched (list)
            watch_list is a list of dictionaries composed of following pairs of keys and values:
                - "url": The URL for the RSS feed. 
                - "journal": Name of journals. The name will be appeared in the slack channel.
                - "color": Hex code. The colour will be used for decolating the post.
                - "thumb": URL for the thumbnail. The picture will be shown with the post.
            The example of watch_list is included in the package (PaperWatchDog/watch_list.py)
        """
        if os.path.exists(self.REGISTERED_URL):
            url_registered = [line.rstrip('\n') for line in open(self.REGISTERED_URL)]
        else:
            url_registered = []
        file_registered_url = open(self.REGISTERED_URL, "a")
        
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)
        slack = slackweb.Slack(url=self.WEBHOOK_URL)
        for dict_journal in watch_list:
        
            name = dict_journal["journal"]
            url_q = dict_journal["url"]
            col = dict_journal["colour"]
            thumb = dict_journal["thumb"]
            rss = feedparser.parse(url_q)
            if len(rss.entries) <=1:
                break
            for one_paper in rss.entries:
                paper = Paper(one_paper)
                try:
                    paper = Paper(one_paper)
                    if verbose: paper.print()                    
                    if paper.url in url_registered:
                        continue
                    paper.arrange_attachment(journal=name, colour=col,thumbnail=thumb)
                    attachments = paper.attachments.copy()
                    slack.notify(attachments=attachments)
                    # Save
                    file_registered_url.write("\n"+paper.url) 
                except:
                    break
                time.sleep(1.2)
        
        file_registered_url.close()
