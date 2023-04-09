import praw
from bdfr.cloner import RedditCloner
from bdfr.configuration import Configuration
from threading import Thread
import json
import os


class archiver():
    def __init__(self, configfile):
        with open(f'{os.getcwd()}\\api\\{configfile}') as config_file:
            config = json.load(config_file)
            config_file.close()
        reddit = praw.Reddit(client_id=config["client_id"],
                             client_secret=config["client_secret"],
                             password=config["password"],
                             user_agent=config["user_agent"],
                             username=config["username"])

        subreddits = "+".join([f"{sub}" for sub in config["subreddits"]])
        #subreddits = config["subreddits"]
        self.subreddit = reddit.subreddit(subreddits)
        self.typeOf = configfile[7:-5]
    def start(self):
        for submission in self.subreddit.stream.submissions(skip_existing=True):
            Thread(target=self.downloader(submission)).start()

    def downloader(self, submission):
        configuration = Configuration(self.typeOf)
        RedditCloner(args=configuration).download(submission)


downloader = archiver(configfile="config-sfw.json")
downloader.start()