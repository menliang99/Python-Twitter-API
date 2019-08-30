#Application Secenario:
#www.ourwebsite.com "login with twitter button"
#They press "Sign in" or "authorize"
#Twitter sends them back to e.g. www.ourwebsite.com/auth
#We get that auth code + request token --> twitter --> access token.


import constants
import oauth2
import urllib.parse as urlparse
import json

#create a consumer, which uses CONSUMER_KEY and CONSUMER_SECRET to identify our app uniquely.
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
client = oauth2.Client(consumer)

#use client to perform a request for the request token
response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
if response.status != 200:
    print("An error occured getting the the request token from twitter.")

#Get the request token parsing the query string returned.
request_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

#Ask user to authorize our app and give us the pin code
print("Go to the following site in your brower: ")
print("{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token']))
oauth_verifier = input("What is the PIN? ")

#Create a token object which contains the request token, and the verifier.
token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)

#Create a client with our consumer and the newly created token
client = oauth2.Client(consumer, token)

#Ask twitter for an access token, and Twitter knows it should give us it because we have verified the request token.
response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))
print(access_token)

#Create an 'authorized_token' Token object and use that to perform Twitter API calls on behalf of the user
authorized_token = oauth2.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
authorized_client = oauth2.Client(consumer, authorized_token)

#Make twitter API calls
response, content = authorized_client.request('https://api.twitter.com/1.1/search/tweets.json?q=hongkong+filter:images', 'GET')
if response.status != 200:
    print("An error occurred when searching!")

tweets = json.loads(content.decode('utf-8'))

for tweet in tweets['statuses']:
    print(tweet['text'])
