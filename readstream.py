from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import json
import requests

def sentimentValue(sentiment):
  if (sentiment == "positive"):
    return(1)
  elif (sentiment == "negative"):
    return(-1)
  else: 
    return(0)

def getLineSentiment(line):
  words = line.lower().split()
  tsent = 0
  for word in words:
    wsent = 0
    try:
      wsent = sentimentValue(dwsent[word.replace("#","").replace("@","")].encode('ascii'))
    except:
      wsent = 0
    finally:
      tsent = tsent + wsent
  if tsent > 0:
    return("positive")
  elif tsent < 0:
    return("negative")
  else:
    return("neutral")

def getShow(line):
  words = line.lower().split()
  tsent = 0
  for word in words:
    try:
      show = shows[word.replace("#","").replace("@","").replace(":","")].encode('ascii')
      return(show)
    except:
      None
  
def getText(line):
  j = json.loads(line);
  return((j["created_at"], j["id"], j["text"]))

def postToSolr(t, rdd):
  solr_url = "http://auisbigdatabox.cloudapp.net:8983/solr/project/update?commitWithin=5000"
  d = json.dumps(rdd.map(lambda x: x).collect())
  print(d)
  h = {'content-type': 'application/json'}
  r = requests.post(solr_url, data=d, headers=h)
  print(r.status_code)
  #r2 = requests.get("http://auisbigdatabox.cloudapp.net:8983/solr/admin/cores?action=RELOAD&core=project_shard1_replica1")
  #print(r2.status_code)


sc = SparkContext()

dwsent = dict(sc.textFile("/data/dictionary.tsv").map(lambda line: line.split("\t")) \
  .map(lambda line: (line[2], line[5])).collect())
shows = dict(sc.textFile("/data/shows.txt").map(lambda line: (line.lower().encode('ascii'), line)).collect())


ssc = StreamingContext(sc, 1)
ds = ssc.textFileStream("/project/rawdata")
ods = ds.window(30, 30).map(lambda line: getText(line)) \
  .map(lambda line: {"created_dt": line[0], "show_s": getShow(line[2]), "sentiment_s": getLineSentiment(line[2]), "text_t": line[2]})
ods.foreachRDD(postToSolr)
  
ssc.start()
ssc.awaitTermination()
