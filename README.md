### real-time tweet sentiment analysis

_Note: Before I got started with this work, I did this [tutorial](http://hortonworks.com/hadoop-tutorial/how-to-refine-and-visualize-sentiment-data/#configure-and-start-solr)_

**Setup**

1. Create new directories and upload files to hdfs

a. /project/twitter_credentials.json

b. /data/dictionary.tsv

c. /data/shows.txt

d. new directory /project/rawdata

2. Follow tutorial to start solr and start ntpd service

3. Follow tutorial on how to create collection in solr. For this project the collection name was "project"

4. Follow tutorial on how to add twitter date format in ParseDateFieldUpdateProcessorFactory in solrconfig.xml

5. Install required packages for python (oauth2, requests, etc)

**Components**

1. Python script to stream tweets to HDFS (stream_to_hdfs.py)
   - This script will get tweets every 30 seconds and save each tweet to a file in /project/rawdata
   - Filename is a random number with 20 digits

2. Python script to read from file and add to solr for indexing (readstream.py)
   - creates a textFileStream reading from /project/rawdata
   - creates an rdd per line/tweet using only fields created_at and text.
   - use text to calculate sentiment and extract show name per rdd
   - create json containing create_dt, show_s, sentiment_s and text_t per rdd
   - post json to solr collection "project" with commitWithin=5000 per rdd

3. HDFS+Spark

4. Solr+Banana
   - Open file "TV Show Sentiment - Time Series-1458052996356" - this is the dashboard for the visualization

**To Run**

Using command line:

```
$ cd coursework
$ spark-submit ./stream_to_hdfs.py
```

In a separate session,
```
$ cd coursework
$ spark-submit ./readstream.py
```

**To Stop**

`ctrl-C`

See our work in action:
https://www.youtube.com/watch?v=KKV7KqaKA6s

See the code:
https://github.com/auimendoza/coursework
