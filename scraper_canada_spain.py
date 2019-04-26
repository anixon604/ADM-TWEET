# Canada Coords SW: 49.003687, -123.222463, NE: 61.239175, -61.879918
# Spain Coords SW: 35.785688, -7.412512, NE: 42.376885, 3.321487
## NOTE!!! LAT/LONG has to be switched to LONG/LAT
## The streaming API doesn't allow to filter by location AND keyword simultaneously.

import os
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import time


class CanadaListener(StreamListener):

    # track canada tweets in Barcelona
    def on_data(self, data):
        print("Canada")
        try:
            with open('CanadaLocationTweets.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


class SpainListener(StreamListener):

    # track canada tweets in Barcelona
    def on_data(self, data):
        print("Spain")
        try:
            with open('SpainLocationTweets.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

# note you must manually set the environment with your credentials

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_secret = os.environ['ACCESS_SECRET']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

canada_stream = Stream(auth, CanadaListener())
canada_stream.filter(locations=[-123.222463, 49.003687, -61.879918, 61.239175], is_async=True)
time.sleep(4800)
canada_stream.disconnect()

spain_stream = Stream(auth, SpainListener())
spain_stream.filter(locations=[-7.412512, 35.785688,  3.321487, 42.376885], is_async=True)
time.sleep(4800)
spain_stream.disconnect()

