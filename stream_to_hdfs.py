import urllib2 as urllib
import oauth2 as oauth
import json
import os
import random
import string
import time
from pyspark import SparkContext

sc = SparkContext()
http_handler  = urllib.HTTPHandler(debuglevel=0)
https_handler = urllib.HTTPSHandler(debuglevel=0)

shows = ["TheAmericansFX", "HouseofCards", "TrueDetective", "FargoFX", "Suits_USA", "BetterCallSaul",
    "AmericanCrimeTV", "DowntonAbbey", "girlsHBO", "broadcity", "TogethernessHBO", "thexfiles",
    "GreysABC", "BigBang_CBS", "TheGrinderFOX", "Castle_ABC", "BONESonFOX", "CrimMinds_CBS",
    "FamilyGuyonFOX", "TheSimpsons", "Nashville_ABC", "TheGoodWife_CBS", "SiliconHBO",
    "WalkingDead", "LastManABC", "SleepyHollowFOX", "alwayssunny", "HowToGetAwayABC",
    "CSICyber","supergirlcbs","EmpireFOX","LastManFOX","NewGirlonFOX","NBCBlacklist",
    "AmericanDadTBS", "ArcherFX", "BasketsFX", "SHO_Homeland", "LastWeekTonight",
    "WorkaholicsCC"]

scred = sc.textFile("/project/twitter_credentials.json")
cred = scred.collect()
tc = json.loads("".join(cred))

oauth_token = oauth.Token(key=tc["access_token_key"], secret=tc["access_token_secret"])
oauth_consumer = oauth.Consumer(key=tc["api_key"], secret=tc["api_secret"])
signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

def twitter_request(url, http_method, parameters):
    req = oauth.Request.from_consumer_and_token(oauth_consumer, token=oauth_token, http_method=http_method,
                                             http_url=url, parameters=parameters)
    req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

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

def stream_tweets(max_tweets=5000):
    url = "https://stream.twitter.com/1.1/statuses/filter.json"

    parameters = {"track": ",".join(shows)}
    response = twitter_request(url, "GET", parameters)

    line_count = 0

    for line in response:
        newfilename = ''.join(random.SystemRandom().choice(string.digits) for _ in range(20))
        line_count += 1
        linerdd = sc.parallelize([line.strip()])
        linerdd.saveAsTextFile("/project/rawdata/" + newfilename)
        time.sleep(30)
        if line_count >= max_tweets:
            exit()

if __name__ == "__main__":
  stream_tweets()
