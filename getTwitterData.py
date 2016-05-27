#get twitter data

import oauth2 as oauth
import urllib2 as urllib

import tweepy 
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

api_key = "YmUa2yPoJblxQe3kdqAKrLxJV"
api_secret = "fd96jpDX8ZJDpzDiVqzR07dgiDwxHZAdj6Rmyx7Y7jFv5nJNnr"
access_token_key = "106773028-VSyLlp7CZHlK7dV1TQNojkrX0UOKtJkuUzxeMGbC"
access_token_secret = "D0gSFHr1C53quAsNdtZCmKPctyjhullTGdBkA838Udcss"

_debug = 0

oauth_token = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"

http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

# Construct, sign, and open a twitter request using the hard-coded credentials above.

def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)
  
  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
# Getting tweets about AI
  url = "https://api.twitter.com/1.1/search/tweets.json?q=%23AI"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
	print line.split()
    
if __name__ == '__main__':
  fetchsamples()


