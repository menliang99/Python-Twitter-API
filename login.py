#Application Secenario:
#www.ourwebsite.com "login with twitter button"
#They press "Sign in" or "authorize"
#Twitter sends them back to e.g. www.ourwebsite.com/auth
#We get that auth code + request token --> twitter --> access token.


import requests

from database import Database
from twitter_utils import get_request_token, get_oauth_verifier, get_access_token
from user import User
from tweets import Twitter

Database.initialise(user='postgres', password='menliang99', host='localhost', database='learning')

screen_name = "Liang26545196"
user = User.load_from_db_by_screen_name(screen_name)

if not user:

    request_token = get_request_token()

    oauth_verifier = get_oauth_verifier(request_token)

    access_token = get_access_token(request_token, oauth_verifier)

    screen_name = input("Enter your screen name : ")
    user = User(screen_name, access_token['oauth_token'], access_token['oauth_token_secret'], None)
    user.save_to_db()

theme = "Hong Kong"
tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q={}&lang=en&result_type=mixed&count=100'.format(theme))
tweet_texts = [{'tweet': tweet['text'], 'label': 'neutral'} for tweet in tweets['statuses']]

for tweet in tweet_texts:
    twitter = Twitter(user.screen_name, theme, tweet['tweet'], tweet['label'], None)
    twitter.analyst()
    twitter.save_to_db()



