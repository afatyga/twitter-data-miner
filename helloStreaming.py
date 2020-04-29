from __future__ import absolute_import, print_function

from tweepy import OAuthHandler, Stream, StreamListener

import json

import keys

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key= keys.consumer_key
consumer_secret=keys.consumer_secret

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token=keys.access_token
access_token_secret=keys.access_secret

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        JSONdata = json.loads(data)
        # if (JSONdata["coordinates"] != None):
        #     print(JSONdata["coordinates"])
        print(JSONdata.get("user", {}).get("location", {}))
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['coca cola'])