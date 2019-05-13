
A slack bot for RSS feeds from academic journals
------------------------------------------------

A python program that retrieves feeds from journals and post to a slack channel.

![](https://raw.githubusercontent.com/skojaku/slack-rss-bot/master/image/slack.png) 


# How to use it

- Create your incoming Webhook in Slack from ![here](https://sada-papers.slack.com/apps/new/A0F7XDUAZ--incoming-webhook-)
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
  
