import praw
from django.conf import settings

class RedditAPI:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=settings.REDDIT_CLIENT_SECRET,
            user_agent=settings.REDDIT_USER_AGENT
        )
        self.mock = False

    def fetch_hot_posts(self, city):
        if self.mock:
            return [
                "The problem isnt Kathmandu, its the whole country. The country is forcing everyone to move to kathmandu. The city does not have the infrastructure to manage this population. Rules are there but no one enforces. Nepal needs to desperately make a campaign of reverse migration from Kathmandu.",
                "This is completely irrelvant to the topic of discussion here. But I've noticed your posts for a few days and everytime I can sniff AI.",
                "Kathmandu is experiencing increasing pollution, posing greater health risks."
            ]
        subreddit = self.reddit.subreddit(city)
        hot_posts = subreddit.hot(limit=10)
        return hot_posts