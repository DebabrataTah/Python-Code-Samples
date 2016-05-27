
# coding: utf-8

# In[68]:

#!/usr/bin/env python


from __future__ import unicode_literals

import logging
import urllib
import urlparse

import json
from collections import OrderedDict

import requests

LOG = logging.getLogger('sw.google_search')


def _decode_response(json_string):
    response = json.loads(json_string)

    meta = {key: value for key, value in response.items() if key != 'items'}
    num_results = int(meta['searchInformation']['totalResults'])
    if num_results == 0:
        LOG.info("No search results.")
        LOG.info(json.dumps(response, indent=4))
        return []
    else:
        LOG.info("{} results.".format(num_results))

    for item in response['items']:
        item['meta'] = meta

    return response['items']


def _strip_protocol(url):
    """
    >>> _strip_protocol('http://foo.bar/blah.x?baz=10&bob=15;x')
    u'foo.bar/blah.x?baz=10&bob=15;x'
    """
    p = urlparse.urlparse(url)
    new_url = urlparse.urlunparse(
        ('', p.netloc, p.path, p.params, p.query, p.fragment))
    return new_url.lstrip('/')


class GoogleCustomSearch(object):
    def __init__(self, search_engine_id, api_key):
        self.search_engine_id = search_engine_id
        self.api_key = api_key

    def search(self, keyword, site=None, max_results=100):
        assert isinstance(keyword, basestring)

        for start_index in range(1, max_results, 10):  # 10 is max page size
            url = self._make_url(start_index, keyword, site)
            logging.info(url)

            response = requests.get(url)
            if response.status_code == 403:
                LOG.info(response.content)
            response.raise_for_status()
            for search_result in _decode_response(response.content):
                yield search_result
                if 'nextPage' not in search_result['meta']['queries']:
                    print("No more pages...")
                    return

    def _make_url(self, start_index, keyword, restrict_to_site):

        if restrict_to_site is not None:
            keyword = 'site:{} {}'.format(_strip_protocol(restrict_to_site),
                                          keyword)
        # https://developers.google.com
        # /custom-search/json-api/v1/reference/cse/list
        params = OrderedDict([
            ('cx', self.search_engine_id),
            ('key', self.api_key),
            ('rsz', '10'),
            ('num', '10'),
            ('googlehost', 'www.google.com'),
            ('gss', '.com'),
            ('q', keyword),
            ('oq', keyword),
            ('filter', '0'),  # duplicate content filter, 1 | 0
            ('safe', 'off'),  # strict | moderate | off
        ])
        #if restrict_to_site is not None:
        #    params['siteSearch'] = _strip_protocol(restrict_to_site)

        return 'https://www.googleapis.com/customsearch/v1?{}'.format(
            urllib.urlencode(params))


# In[69]:

from setuptools import setup, find_packages

long_desc = """
Use the Google Custom Search API to search the web from Python.
"""
# See https://pypi.python.org/pypi?%3Aaction=list_classifiers for classifiers

setup(
    name='google-search',
    version='1.0.0',
    description="Use the Google Custom Search API to search the web.",
    long_description=long_desc,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
    ],
    keywords='',
    author='ScraperWiki Limited',
    author_email='feedback@scraperwiki.com',
    url='http://scraperwiki.com',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=False,
    zip_safe=False,
    install_requires=[
        'requests>=1.2.3',
    ],
    tests_require=[],
    entry_points=\
    """
    """,
)


# In[ ]:

from google_search import GoogleCustomSearch


SEARCH_ENGINE_ID = os.environ['SEARCH_ENGINE_ID']                           
API_KEY = os.environ['GOOGLE_CLOUD_API_KEY']

api = GoogleCustomSearch(SEARCH_ENGINE_ID, API_KEY)

for result in api.search('pdf', 'http://scraperwiki.com'):
    print(result['title']) 
    print(result['link']) 
    print(result['snippet']) 


# In[72]:

#!pip install -U google-api-python-client

#!/usr/bin/env python

import datetime as dt
import json, sys
from apiclient.discovery import build


if __name__ == '__main__':
    # Create an output file name in the format "srch_res_yyyyMMdd_hhmmss.json"
    now_sfx = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = './Downloads/'
    output_fname = output_dir + 'srch_res_' + now_sfx + '.json'
 
    search_term = raw_input("What would you like to search: ")
    num_requests = int(raw_input("How many number of results you need: "))
    #   search_term = sys.argv[1]
     #   num_requests = int(sys.argv[2])

    # Key codes we created earlier for the Google CustomSearch API
    search_engine_id = '013758094297543913661:d4s1vjpzu8k'
    api_key = 'AIzaSyDVtwoqQuLzlw0c_ownnnLvwNx79FVS5fE'
    
    # The build function creates a service object. It takes an API name and API 
    # version as arguments. 
    service = build('customsearch', 'v1', developerKey=api_key)
    # A collection is a set of resources. We know this one is called "cse"
    # because the CustomSearch API page tells us cse "Returns the cse Resource".
    collection = service.cse()

    output_f = open(output_fname, 'ab')

    for i in range(0, num_requests):
        # This is the offset from the beginning to start getting the results from
        start_val = 1 + (i * 10)
        # Make an HTTP request object
        request = collection.list(q=search_term,
            num=10, #this is the maximum & default anyway
            start=start_val,
            cx=search_engine_id
        )
        response = request.execute()
        output = json.dumps(response, sort_keys=True, indent=2)
        output_f.write(output)
        print('Wrote 10 search results...')

    output_f.close()
    print('Output file "{}" written.'.format(output_fname)) 


# In[ ]:



