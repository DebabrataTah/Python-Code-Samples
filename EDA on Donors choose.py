
# coding: utf-8

# In[1]:

import pyspark as ps


# In[2]:

sc = ps.SparkContext('local')


# In[3]:

#checking for single core
sc.master


# In[5]:

#if import ipdb does not work use pip on commandline
import os,ipdb


# In[6]:

cwd = os.getcwd()


# In[7]:

cwd


# In[8]:

#read csv and doing EDA on data from csv
rdd = sc.textFile('file://' + cwd + '/Downloads/opendata_projects.csv')


# In[9]:

#total number of records
rdd.count()


# In[10]:

#taking header
header = rdd.first()


# In[11]:

#rdd with no header
rdd_no_header = rdd.filter(lambda row:row != header)


# In[12]:

rdd_no_header.first()


# In[13]:

#creating list of columns
header_list = header.split(',')


# In[14]:

#sanity check for records to have correct number of columns
columncount = len(header_list)


# In[15]:

columncount


# In[16]:

rdd_csv = rdd_no_header.map(lambda row: row.split(','))


# In[17]:

rdd_csv.map(lambda row: len(row) != columncount).sum()


# In[18]:

rdd_csv.map(lambda row: len(row) == columncount).sum()


# In[19]:

#trying to reason why the data has incorrect number of columns in some rows and fixing them
import pprint

class RowSplitException(Exception):
    pass

def throw_exception(row):
    if len(row) != columncount:
        row_zip = zip(header_list,row)
        message = pprint.pformat(row_zip)
        raise RowSplitException(message)
    else:
        pass


# In[25]:

rdd_csv.foreach(throw_exception)


# In[20]:

#correcting string data for extra quotes
import csv

rdd_csv_correct = rdd_no_header.map(lambda line: csv.reader([line]).next())


# In[21]:

rdd_csv_correct.foreach(throw_exception)
print "Extra quotes parsed"


# In[22]:

#no duplicates in original rdd
rdd_no_dups = rdd_csv_correct.map(lambda row: str(row)).distinct()


# In[23]:

rdd_no_dups.count()


# In[24]:

rdd_csv_correct.map(lambda row: str(row)).distinct().count()


# In[25]:

#creating a dictionary for easy column access and data type changes
rdd_dict = rdd_csv_correct.map(lambda row: dict(zip(header_list, row)))
rdd_dict.first()


# In[26]:

#unique values
rdd_dict.map(lambda row: row['_schoolid']).countApproxDistinct()


# In[27]:

rdd_dict.map(lambda row: row['_schoolid']).distinct().count()


# In[28]:

rdd_dict.map(lambda row: row['total_price_excluding_optional_support']).countApproxDistinct()


# In[29]:

#missing column values
accum = sc.accumulator(0)


# In[30]:

from collections import Counter

class CounterAccumulatorParam(ps.accumulators.AccumulatorParam):
    def zero(self, initialValue):
        return Counter()
    
    def addInPlace(self, v1, v2):
        v1 += v2
        return v1


# In[31]:

accum = sc.accumulator(Counter(), CounterAccumulatorParam())


# In[32]:

def count_null(record):
    global accum
    
    c = Counter()
    
    for key, value in record.items():
        if value =='':
            c[key] +=1
            
    accum.add(c)
        


# In[33]:

rdd_dict.foreach(count_null)


# In[39]:

accum.value


# In[34]:

#type conversion
from pyspark.sql.types import *
from datetime import datetime


# In[35]:

rdd_dict.map(lambda d: (d['teacher_ny_teaching_fellow'], 1)).reduceByKey(lambda a, b: a + b).collect()


# In[36]:

def quote_strip(field):
    return field.strip('"')


# In[80]:

from datetime import datetime

def date_parse(datestring):
    try:
        return None if datestring == '' else str(datetime.strptime(datestring, '%Y-%m-%d'))
    except ValueError:
        print datestring


# In[81]:

def boolean_map(field):
    if field == 't':
        return True
    elif field == 'f':
        return False
    else:
        None


# In[82]:

type_conversion_func = {
    'id': quote_strip,
    'date': date_parse,
    'boolean': boolean_map,
    'float': lambda x: None if x == '' else float(x),
    'integer': lambda x: None if x == '' else int(x),
    'string': lambda x: None if x == '' else x
}


# In[84]:

types = [
    StringType(),
    StringType(),
    StringType(),
    StringType(),
    FloatType(),
    FloatType(),
    StringType(),
    StringType(),
    StringType(),
    StringType(),
    StringType(),
    StringType(),
    BooleanType(),
    BooleanType(),
    BooleanType(),
    BooleanType(),
    BooleanType(),
    BooleanType(),
    StringType(),
    BooleanType(),
    BooleanType(),
    StringType(),
    StringType(),
    StringType(),
    StringType(),
    StringType(),
    StringType(),
    StringType(),
    FloatType(),
    FloatType(),
    FloatType(),
    FloatType(),
    FloatType(),
    FloatType(),
    FloatType(),
    FloatType(),
    FloatType(),
    BooleanType(),
    BooleanType(),
    StringType(),
    DateType(),
    DateType(),
    DateType(),
    DateType()
]


# In[88]:

column_type_lookup = dict(zip(header_list, types))
column_type_lookup


# In[89]:

#creating data frame
import json

def convert_types(d):
    for field in d:
        if field[0] == "_":
            transform = type_conversion_func['id']
        else:
            transform = type_conversion_func[column_type_lookup[field].typeName()]
        
        d[field] = transform(d[field])
        
    return json.dumps(d)


# In[90]:

rdd_typed = rdd_dict.map(convert_types)


# In[91]:

rdd_typed.take(1)


# In[92]:

from pyspark.sql import Row

sqlContext = ps.HiveContext(sc)


# In[93]:

#infer schema
df = sqlContext.jsonRDD(rdd_typed)


# In[94]:

df.printSchema()

structs = map(lambda x: StructField(*x), zip(header_list, types))
schema = StructType(structs)
schema.fields

df_force = sqlContext.jsonRDD(rdd_typed, schema=schema)
#force schema
df_force.printSchema()


# In[95]:

# when schema forced, dates convert correctly
df_force.first()

df_force.show()


# In[96]:

# subselect relevant columns
df_subselect = df_force.select('school_city', 'primary_focus_area',                                df_force['resource_type'].alias('resource'),                                'poverty_level','grade_level',                                df_force['total_price_excluding_optional_support'].alias('p_exclude'),                                df_force['total_donations'].alias('total_d'),                                df_force['funding_status'].alias('status'))


# In[97]:

df_subselect.show()


# In[98]:

#null value check
df_force.filter(df_force['students_reached'].isNull()).select('students_reached', 'funding_status').collect()


# In[99]:

df_no_null = df_force.fillna(0, ['students_reached'])


# In[100]:

#frequent items - 70% apprearence
freq_items = df_no_null.freqItems(['school_city', 'primary_focus_area',                                      'grade_level', 'poverty_level','resource_type'], 0.7).collect()


# In[101]:

freq_items[0]


# In[102]:

df_no_null.freqItems(['num_donors'], .3).collect()[0]


# In[103]:

#distributions
df_no_null.groupby('funding_status').count().show()


# In[104]:

df_complete = df_no_null.filter(df_no_null['funding_status'] == 'completed')
df_expired = df_no_null.filter(df_no_null['funding_status'] == 'expired')


# In[105]:

df_complete.write.json('file://' + cwd + '/data/donors_choose/opendata_completed.json')
df_expired.write.json('file://' + cwd + '/data/donors_choose/opendata_expired.json')


# In[106]:

df_complete.groupby('num_donors').count().write.json('file://' + cwd + '/data/donors_choose/num_donors_completed.json')
df_expired.groupby('num_donors').count().write.json('file://' + cwd + '/data/donors_choose/num_donors_expired.json')


# In[107]:

get_ipython().system(u'du -h data/')


# In[108]:

#summary statistics
df_no_null.select('total_donations', 'num_donors', 'students_reached',                   df_no_null['total_price_excluding_optional_support'].alias('p_exclude'),                   df_no_null['total_price_including_optional_support'].alias('p_include'))           .describe().show()


# In[109]:

price_rdd = df_no_null.select('total_price_excluding_optional_support').rdd.map(lambda r: r.asDict().values()[0])


# In[110]:

# massive outliers, will skew histogram buckets
outliers = price_rdd.top(3)
outliers


# In[111]:

# for continuous columns we can use Histogram RDD function
hist = price_rdd.filter(lambda x: x not in outliers).histogram(100)


# In[112]:

hist


# In[113]:

import matplotlib.pyplot as plt
import pandas as pd

get_ipython().magic(u'pylab inline')


# In[114]:

def plot_rdd_hist(hist):
    idx = []

    for i in range(len(hist[0]) - 1):
        idx.append((hist[0][i] + hist[0][i+1])/ 2)
        
    pd.DataFrame({'counts': hist[1], 'index': idx}).set_index('index').plot(figsize=(16,5))


# In[115]:

cheap_histogram = price_rdd.filter(lambda x: x < 5000).histogram(100)


# In[116]:

cheap_histogram


# In[117]:

plot_rdd_hist(cheap_histogram)


# In[118]:

plot_rdd_hist(price_rdd.filter(lambda x: x < 30000).histogram(100))


# In[120]:

from IPython.display import IFrame

IFrame('http://bl.ocks.org/Jay-Oh-eN/raw/c532c8703547cf148006/d7c0db2150bdde2a56acce2456a5bbe19527a79b/', width=960, height=500)


# In[121]:

def spark_histogram(df, column):
    donor_counts = df.groupby(column).count()
    donor_df = donor_counts.toPandas()
    donor_df[column] = donor_df.num_donors.astype(float)
    return donor_df.sort(column).set_index(column).iloc[:50,:].plot(kind='bar', figsize=(14,5))


# In[122]:

spark_histogram(df_complete, 'num_donors')


# In[123]:

spark_histogram(df_expired, 'num_donors')


# In[124]:

# categorical/boolean fields can give valuable facets (crosstabs) 
#correlations between columns
df_no_null.crosstab('school_charter', 'funding_status').show()
df_no_null.crosstab('school_magnet', 'funding_status').show()
df_no_null.crosstab('school_metro', 'funding_status').show()
df_no_null.crosstab('poverty_level', 'funding_status').show()
df_no_null.crosstab('grade_level', 'funding_status').show()


# In[125]:

df_no_null.crosstab('resource_type', 'funding_status').show()
df_no_null.crosstab('primary_focus_area', 'resource_type').show()


# In[126]:

df_no_null.stat.corr('total_price_excluding_optional_support', 'num_donors')


# In[127]:

df_no_null.stat.corr('total_price_excluding_optional_support', 'students_reached')


# In[128]:

df_no_null.stat.corr('total_price_excluding_optional_support', 'total_price_including_optional_support')


# In[ ]:



