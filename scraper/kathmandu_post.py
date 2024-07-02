import requests
from bs4 import BeautifulSoup
import re
# import tweepy
# import praw


# Define the URL
url = "https://kathmandupost.com/national"

# Send a GET request to the URL
response = requests.get(url)
response.raise_for_status()  # Raise an exception for HTTP errors

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')


# Find all divs with the class 'article-image'
articles = soup.find_all('article', class_='article-image')

# Extract the text of h3 inside each div
news_all = [article.find('a').get("href") for article in articles]

pattern = r'^/(.*?)/(\d{4}/\d{2}/\d{2})/(.*)$'
for news in news_all:
    match = re.match(pattern, news)
    if match:
        category = match.group(1)
        date = match.group(2)
        title = match.group(3).replace('-', ' ')
        print(f"News: {news}")
        print(f"Category: {category}")
        print(f"Date: {date}")
        print(f"Title: {title}")
        print(f"----------------")
    else:
        print("The URL format is incorrect.")


def twitter():
    auth = tweepy.OAuth1UserHandler('YOUR_CONSUMER_KEY', 'YOUR_CONSUMER_SECRET', 'YOUR_ACCESS_TOKEN', 'YOUR_ACCESS_TOKEN_SECRET')
    api = tweepy.API(auth)

    query = 'Maternity hospital mental health screening'
    for tweet in tweepy.Cursor(api.search_tweets, q=query).items(10):
        print(tweet.user.screen_name, tweet.text)


def reddit():
    reddit = praw.Reddit(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET', user_agent='YOUR_USER_AGENT')

    query = 'Maternity hospital mental health screening'
    subreddits = reddit.subreddits.search(query)

    for subreddit in subreddits:
        print(subreddit.display_name, subreddit.title)


def facebook():
    access_token = 'EAAEsRtHbU8EBO2gXWle2F3XvybC1P8gOaDWJRn9UVZAZA26wq87J93HZBrZAK6pPhTJZBb7FUfbZBICsjFPrZAhqvQ0rDS883vQWqJc6n3lnyJHZA3E48fZAm8qZCpZCEWJzCGlTySvbPZC2EHNJbZCwn4176dYTgZAaM6419oHH0qqRajTsEWMl2r44j2l3Wb8hBBhYxaqNIXIp3unHMGU0YhUP3A453998NKEpTb1UiSTSLpeW5Xa5ZApgl6pNMLtCI0oPwZDZD'
    query = 'Maternity hospital mental health screening'
    url = f'https://graph.facebook.com/v14.0/search?type=group&q={query}&access_token={access_token}'

    response = requests.get(url)
    data = response.json()
    print(data)
    for group in data['data']:
        print(group['name'], group['id'])

facebook()

