import praw
from django.conf import settings

class RedditAPI:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id='M1jJbvYlxLJRRJRjFFYDbg',
            client_secret='T1Lkv1uoLdRYdUN9BtCbCbbLBhFwgw',
            user_agent='mlexperts'
        )
    
    def fetch_hot_posts(self, topic):
        subreddit = self.reddit.subreddit(topic)
        hot_posts = subreddit.hot(limit=10)
        return [
            "The problem isnt Kathmandu, its the whole country. The country is forcing everyone to move to kathmandu. The city does not have the infrastructure to manage this population. Rules are there but no one enforces. Nepal needs to desperately make a campaign of reverse migration from Kathmandu."
            "This is completely irrelvant to the topic of discussion here. But I've noticed your posts for a few days and everytime I can sniff AI."
        ]