# Written by Sadamori Kojaku 
#
# References:
# https://qiita.com/TatsuyaMizuguchi17/items/35dd3dd1396864006031
#

import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import feedparser 
import time
import slackweb
import datetime as dt

# Configulation =====================
# List of urls being sent to slack
REGISTERED_URL = ".registered_urls.txt"

# slack webhook URL
WEBHOOK_URL = "add your slack webhook url"

# List of journals being fetched 
url_q_list = [
    {
        "journal": "arXiv (Physics Soc Ph)",
         "url": "http://export.arxiv.org/rss/physics.soc-ph",
         "colour": "#2eb886",
         "thumb": "https://pbs.twimg.com/profile_images/958432197987401728/QLeEVLC__400x400.jpg",
    },
    {
        "journal":"SIAM", 
        "url":'https://epubs.siam.org/action/showFeed?jc=SMJMAP&type=etoc&feed=rss', 
        "colour":"#2EACA0", 
	"thumb": "https://www.siam.org/Portals/0/Images/SIAM_Logo/SIAM_3272.png?ver=2018-09-25-172036-313"
    },
    {
        "journal":"Phys. Rev. Letters", 
        "url":'http://feeds.aps.org/rss/recent/prl.xml', 
        "colour":"#517E65", 
        "thumb":"https://pbs.twimg.com/profile_images/676479054359302144/uEaYfqZP_400x400.png"
    },
    {
        "journal":"Phys. Rev. E", 
        "url":'http://feeds.aps.org/rss/recent/pre.xml', 
        "colour":"#946038", 
        "thumb":"https://pbs.twimg.com/profile_images/831546995273719809/c6AeMWXn_400x400.jpg"
    },
    {
        "journal":"Nature", 
        "url":'http://feeds.nature.com/nature/rss/current?format=xml', 
        "colour":"#9C1A1A", 
        "thumb":"https://qutech.nl/wp-content/uploads/2018/02/nature-journal-559x280.jpg"
    },
    {
        "journal":"Sci. adv.", 
        "url":'https://advances.sciencemag.org/rss/current.xml', 
        "colour":"#000000", 
        "thumb":"https://pbs.twimg.com/profile_images/887051732613820418/uOQVGEqX_400x400.jpg"
    },
    {
        "journal":"PNAS", 
        "url":'http://feeds.feedburner.com/Pnas-RssFeedOfEarlyEditionArticles?format=xml', 
        "colour":"#2661A3", 
        "thumb":"https://pbs.twimg.com/profile_images/1049315013603672064/d4ngrZC__400x400.jpg"
    },
    {
        "journal":"Sci. Rep.", 
        "url":'http://feeds.nature.com/srep/rss/current?format=xml', 
        "colour":"#CEDDE4", 
        "thumb":"https://www.nature.com/content/scirep-facts/images/header_title.png"
    }
]
# ===================================

url_registered = [line.rstrip('\n') for line in open(REGISTERED_URL)]
file_registered_url = open(REGISTERED_URL, "a")

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)
slack = slackweb.Slack(url=WEBHOOK_URL)

#論文ごとのクラス
class Entry():

    def __init__(self,entry):
        #著者、URL、タイトル、要約を取得。
        #authors = [re.sub("<.+?>","",a) for a in entry.author.split(", ")]
        #authors = [re.sub("<.+?>","",a) for a in entry.author.split(", ")]
        #self.author=authors[0]
        if entry.id.find("arxiv")>=0:
            isarXiv = True

        if isarXiv:
            authors = [re.sub("<.+?>","",a) for a in entry.author.split(", ")]
            self.author = authors[0] 
            for i in range(1,len(authors)):
                self.author="%s, %s" % (self.author, authors[i])
        else:
            self.author = entry.authors[0]["name"]
            for i in range(1,len(entry.authors)):
                self.author="%s, %s" % (self.author, entry.authors[i]["name"])
                #self.author="%s, %s" % (self.author, authors[i])
        self.url = entry.id
        self.title = re.sub(" \(arXiv:.+\)$","",entry.title)
        self.author_info = {}

    def arrange_attachment(self, journal="", colour="#ffffff", thumbnail=""):
        self.attachments = [
            {
                "fallback": "Required plain-text summary of the attachment.",
                "color": colour,
                "fields": [
                    {
                        "value": journal+"\n"+self.title+"\n"+self.author+"\n"+self.url,
                        "short": False
                    }
                ],
                "image_url": "",
                "thumb_url": thumbnail
            }
        ]


for dict_journal in url_q_list:

    name = dict_journal["journal"]
    url_q = dict_journal["url"]
    col = dict_journal["colour"]
    thumb = dict_journal["thumb"]
    rss = feedparser.parse(url_q)
    if len(rss.entries) <=1:
        break
    for one_entry in rss.entries:
        try:
            entry = Entry(one_entry)
           
            if entry.url in url_registered:
                continue
            entry.arrange_attachment(journal=name, colour=col,thumbnail=thumb)
            attachments = entry.attachments.copy()
            slack.notify(attachments=attachments)
            # Save
            file_registered_url.write("\n"+entry.url) 
        except:
            break
        time.sleep(1.2)

file_registered_url.close()
