
# coding: utf-8

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
    num_requests = int(raw_input("Specify the offset: "))
    #   search_term = sys.argv[1]
     #   num_requests = int(sys.argv[2])

    # Key codes we created earlier for the Google CustomSearch API
    search_engine_id = 'Engine id'
    api_key = 'server key'
    
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



