#Application Secenario:
#www.ourwebsite.com "login with twitter button"
#They press "Sign in" or "authorize"
#Twitter sends them back to e.g. www.ourwebsite.com/auth
#We get that auth code + request token --> twitter --> access token.


import constants
import oauth2
import urllib.parse as urlparse
from user import User
from database import Database
from twitter_utils import consumer, get_request_token, get_oauth_verifier, get_access_token

Database.initialise(user='postgres', password='menliang99', host='localhost', database='learning')

user_email = input("Enter your email address: ")
user = User.load_from_db_by_email(user_email)

if not user:

    request_token = get_request_token()

    oauth_verifier = get_oauth_verifier(request_token)

    access_token = get_access_token(request_token, oauth_verifier)

    email = input("Enter you email : ")
    first_name = input("Enter your first name : ")
    last_name = input("Enter your last name : ")

    user = User(email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'], None)
    user.save_to_db()

tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=hongkong+filter:images')
for tweet in tweets['statuses']:
    print(tweet['text'])

