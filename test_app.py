import setup
import searchTerms

searchTerms.calibrate()

def test_getmsg():
    assert searchTerms.getMsgs("covid", 1) == [[3, 40.7127281, -74.0060152, 'New York City, NY'], [3, 40.7127281, -74.0060152, 'New York City, NY']] #tests using jsons file of tweets

def remove_noise():
    assert searchTerms.remove_noise("@Trump is really dumb") == "is really dumb"    #able to parse out #

def test_sent():
    assert searchTerms.get_tweet_sentiment("terrible, I despise today") == 3        #test negative tweet
    assert searchTerms.get_tweet_sentiment("i am having a good day!") == 1          #test positive tweet
    



