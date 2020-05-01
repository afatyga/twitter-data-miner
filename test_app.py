import searchTerms

def test_getmsg():
    assert searchTerms.getMsgs("covid", 1) == [[3, 40.7127281, -74.0060152, 'New York City, NY'], [3, 40.7127281, -74.0060152, 'New York City, NY']]
[40.7127281, -74.0060152, 40.7127281, -74.0060152]]
    
def test_sent():
    assert searchTerms.get_tweet_sentiment("terrible, I despise today") == 3
    assert searchTerms.get_tweet_sentiment("goood, I reaLLY LIKE CHOCOLATE CAKE") == 1
    assert searchTerms.get_tweet_sentiment("@happy you are really dumb") == 3

def remove_noise():
    assert searchTerms.remove_noise("@Trump is really dumb") == "Trump is really dumb"

