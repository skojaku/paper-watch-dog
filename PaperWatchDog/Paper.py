import re

#Paper class
class Paper():

    def __init__(self,paper):
        """
        Extract the attributes of the paper from the RSS. 
        """
        isarXiv = False
        if paper.id.find("arxiv")>=0:# archive requires an exceptional parsing logics
            isarXiv = True
        if isarXiv: 
            authors = [re.sub("<.+?>","",a) for a in paper.author.split(", ")]
            self.author = authors[0] 
            for i in range(1,len(authors)):
                self.author="%s, %s" % (self.author, authors[i])
        else:
            print("___________")
            if "authors" in paper:
                if len(paper.authors[0])==0:
                    self.author = "author unknown"
                else:
                    self.author = paper.authors[0]["name"]
                    for i in range(1,len(paper.authors)):
                        self.author="%s, %s" % (self.author, paper.authors[i]["name"])
                        #self.author="%s, %s" % (self.author, authors[i])
            else:
                self.author = "author unknown"
            print(self.author)
        self.url = paper.id
        self.title = re.sub(" \(arXiv:.+\)$","",paper.title)
        self.author_info = {}

    def print(self):
        print("{author} {title} {url}".format(author=self.author, title=self.title, url=self.url))

    def arrange_attachment(self, journal="", colour="#ffffff", thumbnail=""):
        self.attachments = [
            {
                "fallback": "{author} {title} {journal}".format(author =self.author, title = self.title, journal = journal),
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
