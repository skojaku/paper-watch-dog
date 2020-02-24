
A Watch Dog for academic papers in your slack channles 
------------------------------------------------

![](https://raw.githubusercontent.com/skojaku/paper-watach/dog/master/image/slack.png) 


# How to use it

- Create the Webhook URL from [here](https://api.slack.com/messaging/webhooks )
- Open the example.py and paste the url to the `WEBHOOK_URL` variable:

```python 
# slack webhook URL
WEBHOOK_URL = "https://hooks.slack.com/services/****************"
```

All done! Run the example.py.

To run WatchDog in daily basis, use the crontab.
For example, 
- make a dictionary called `paper-watch-dog` under the $HOME/.cron directory. 
- Then, copy the example.py to the directory. 
- Edit crontab

```bash
crontab -e
0 12 * * * python3 ~/.cron/paper-watch-dog/example.py
```


# How to make your watch list

- The package comes with a default watch list of journals. You can customize it by your own. 
- One can read the default watch list by

```python
import PaperWatchDog as pwd 
print(pwd.watch_list)
```

- The watch list is a list of dictionaries. Each dictionary takes the following pairs of keys and values:
    - "url": The URL for the RSS feed. 
    - "journal": Name of journals. The name will be appeared in the slack channel.
    - "color": Hex code. The colour will be used for decolating the post.
    - "thumb": URL for the thumbnail. The picture will be shown with the post.

The resulting dictionary looks like:

```python
    {   
        "journal": "arXiv (Physics Soc Ph)",
         "url": "http://export.arxiv.org/rss/physics.soc-ph",
         "colour": "#2eb886",
         "thumb": "https://pbs.twimg.com/profile_images/958432197987401728/QLeEVLC__400x400.jpg",
    },  
```



# Reference
- https://qiita.com/TatsuyaMizuguchi17/items/35dd3dd1396864006031
