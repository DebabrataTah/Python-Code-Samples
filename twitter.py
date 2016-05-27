
# coding: utf-8

# In[7]:

get_ipython().system(u'pip install oauth2 ')
#has to before accessing twitter data


# In[43]:

get_ipython().system(u'pip install tweepy')


# In[47]:

#import oauth2 as oauth
import urllib2 as urllib

import tweepy 
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
#import urllib
#response = urllib.urlopen("https://api.twitter.com/1.1/search/tweets.json?q=microsoft")

#finding how the response looks
#pyresponse = json.load(response)

api_key = "Key"
api_secret = "Secret"
access_token_key = "tokenkey"
access_token_secret = "tokensecret"

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
  url = "https://api.twitter.com/1.1/search/tweets.json?q=%23iosgames"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
    print line.strip()

if __name__ == '__main__':
  fetchsamples()



# In[40]:

from urllib2 import HTTPError, URLError,urlopen, Request

#reads aas string
#response = urllib2.urlopen('https://mommentoring.wordpress.com/')
#html = response.read()

#simulates http request as string
req = urllib2.Request('https://mommentoring.wordpress.com/')
try: 
    response = urllib2.urlopen(req)
except urllib2.HTTPError as e:
    print e.code
    print e.read()
except URLError as e:
    print e.reason
else:
    the_page = response.read()

print type(the_page)


# In[28]:




# In[30]:




# In[33]:




# In[34]:




# In[45]:




# In[46]:




# In[47]:




# In[51]:




# In[ ]:



