
A slack bot for RSS feeds from academic journals
------------------------------------------------

# A python program that retrieves feeds from journals and post to a slack channel.

![](https://raw.githubusercontent.com/skojaku/slack-rss-bot/master/image/slack.png) 


# How to use it

- Create your incoming Webhook in Slack from [here](https://sada-papers.slack.com/apps/new/A0F7XDUAZ--incoming-webhook-)
- Copy Webhook URL and paste it in line 21 in main.py as follows:

```python 
# slack webhook URL
WEBHOOK_URL = "https://hooks.slack.com/services/****************"
```

- Delete all lines in .registered_urls.txt, in which each line indicates the url of a paper. 
The program does not post the paper if already registered in this file, sending only new feeds to your slack channel.

- Place the program to an appropriate place (me place ~/.cron/slack-rss/main.py). Then, set a crontab or other program that routinely runs it, e.g., 

```bash
crontab -e
0 12 * * * python3 ~/.cron/slack-rss/main.py
```


# How to add your favorite journals

- You can add a journal by adding a dict object to `url_q_list` in line 24 in main.py.   

```python
url_q_list = [
    {
        "journal": "journal name",
         "url": "url for the RSS",
         "colour": "side bar colour",
         "thumb": "thumbnail for the journal. Set "" if you don't need it",
    }, ....
```

For example,  

```python
url_q_list = [
    {
        "journal": "arXiv (Physics Soc Ph)",
         "url": "http://export.arxiv.org/rss/physics.soc-ph",
         "colour": "#2eb886",
         "thumb": "https://pbs.twimg.com/profile_images/958432197987401728/QLeEVLC__400x400.jpg",
    }, ....
```

# Reference
- https://qiita.com/TatsuyaMizuguchi17/items/35dd3dd1396864006031
