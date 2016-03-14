import urllib2 as urllib
import oauth2 as oauth
import json
import os

# urlib2 stuff
_debug = 0
http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

# oauth2 stuff
with open(os.path.dirname(__file__) + "/twitter_credentials.json") as f:
    tc = json.load(f)
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


def stream_tweets(track_list, max_tweets=5000):
    url = "https://stream.twitter.com/1.1/statuses/filter.json"

    parameters = {"track": ",".join(track_list)}
    response = twitter_request(url, "GET", parameters)

    line_count = 0
    for line in response:
        line_count += 1
        print line.strip()
        if line_count >= max_tweets:
            exit()
