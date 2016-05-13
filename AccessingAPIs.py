
# coding: utf-8

# In[1]:

get_ipython().system(u'pip install oauth2 ')
#has to before accessing twitter data


# In[2]:

get_ipython().system(u'pip install tweepy')


# In[3]:

#get twitter data

import oauth2 as oauth
import urllib2 as urllib

import tweepy 
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json

api_key = "Key"
api_secret = "Secret"
access_token_key = "tokenKey"
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
# Getting tweets about AI
  url = "https://api.twitter.com/1.1/search/tweets.json?q=%23AI"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
    jsontweet = json.loads(line.strip())
    statustweet = jsontweet['statuses']
    for i in range(10):
        print statustweet[i]["text"]
    
if __name__ == '__main__':
  fetchsamples()



# In[20]:

import urllib2
import json
from urllib2 import HTTPError, URLError,urlopen, Request
from lxml.html import parse
import xml.etree.ElementTree as ET

#reads aas string
#response = urllib2.urlopen('https://mommentoring.wordpress.com/')
#html = response.read()

#simulates http request as string
req = urllib2.Request('https://mommentoring.wordpress.com/about/')
try: 
    response = urllib2.urlopen(req)
except urllib2.HTTPError as e:
    print e.code
    print e.read()
except URLError as e:
    print e.reason
else:
    the_page = response.read()
#    print the_page

tree = ET.parse(response)
root = tree.getroot()

print root
#print p.xpath('//body')[0].text_content()


# GET https://www.googleapis.com/customsearch/v1?key=INSERT_YOUR_API_KEY&cx=017576662512468239146:omuauf_lfve&q=lectures
# 

# In[24]:

#Sending request to google search engine and getting results from there
from googlesearch import GoogleSearch
from pprint import pprint

gs = GoogleSearch('Neelu')
for hit in gs.top_results():
    pprint(hit)
    print


# In[23]:

#install google and pygoogle
get_ipython().system(u'pip install google')
get_ipython().system(u'pip install pygoogle')


# In[31]:

import google
#from google import gsearch
import math,sys
import json
import urllib

def gsearch(searchfor):
  query = urllib.urlencode({'q': searchfor})
  url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s' % query
  search_response = urllib.urlopen(url)
  search_results = search_response.read()
  results = json.loads(search_results)
  data = results['responseData']
  return data

result = gsearch('Neelu')
print type(result)


# In[32]:

#manage your installation
get_ipython().system(u'pip install --upgrade google-api-python-client')


# In[33]:

get_ipython().system(u'pip install lxml==3.6.0')
get_ipython().system(u'pip install matplotlib==1.5.1')
get_ipython().system(u'pip install mysqldb==1.2.5')
get_ipython().system(u'pip install numpy==1.11.0')
get_ipython().system(u'pip install PIL==3.2.0')
get_ipython().system(u'pip install crcmod==2.7')


# In[34]:

get_ipython().system(u'pip install pycrypto==2.6.1')


# In[1]:

# opens a new tab in web browser and searches the requested data
import webbrowser

#used to create new tab
new=2

#specifies the URL
taburl="http://google.com/?#q="

#gets input from user
term = raw_input("Enter search query: ")

#opens the browser
webbrowser.open(taburl+term,new=new)


# In[67]:

get_ipython().system(u'pip install mechanize')
get_ipython().system(u'pip install bs4')

# opens a new tab in web browser and searches the requested data
import urllib
import mechanize
from bs4 import BeautifulSoup
import re

def getGoogleLinks(link,depth):
    #tprepare browser
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders=[('User-agent','chrome')]

    #prepare query
    #term = raw_input("Enter search query: ")
    trm = link.replace(" ","+")
    query="http://google.com/search?num=10&q="+trm+"&start="+depth

    #request the browser
    htmltext = br.open(query).read()
    soup = BeautifulSoup(htmltext)

    search = soup.findAll('div',attrs={'id':'search'})
    searchtext = str(search[0])

    soup1 = BeautifulSoup(searchtext)
    list_items = soup1.findAll('li')
    
    regex= "q(?!.*http).*?&amp"
    pattern = re.compile(regex)

    results_array = []
    for li in list_items:
        soup2 = BeautifulSoup(str(li))
        links = soup2.findAll('a')
        if len(links)>0:
            source_link = links[0]
            source_url = re.findall(pattern,str(source_link))
            if len(source_url) > 0:
                results_array.append(("http://"+str(source_url[0].replace("q=","").replace("&amp","").replace("related:",""))).split('+')[0])
            
    return results_array

print getGoogleLinks("Artificial Intelligence Robots","0")


# In[ ]:



