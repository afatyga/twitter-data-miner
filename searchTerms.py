import keys #holds the keys for using tweepy
import tweepy #twitter api
from geopy.geocoders import Nominatim
import json
import re, string
import os #to get pid id
import helloStreaming

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier

import datetime
global classifier

numTweets = 1000 #num of tweets to get from tweepy
# datetime object containing current date and time

import re, string, random

liveLimit = 15
liveList = []

def getLiveMsgs(searchTerm):
	l = StdOutListener()
	auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
	auth.set_access_token(keys.access_token, keys.access_secret)

	stream = tweepy.Stream(auth, l)
	stream.filter(track=[searchTerm])
	return liveList

def getMsgs(searchTerm, time):
	if not isinstance(searchTerm,str): #can only take in a string
		return []

	if (keys.consumer_key == ""): #meaning all are empty => should read backupTweets.json!

		listOfLinks  = []
		with open('backupTweets.json') as json_file:
			data = json.load(json_file)
			for tweets in data['tweets']:
				try:
					loc = str(tweets['location'])
					if(loc != "None"):
						agent = "dataMining" + str(os.getpid())
						geolocator = Nominatim(user_agent=agent, timeout=3)
						location = geolocator.geocode(loc)
						statusLocList = [get_tweet_sentiment(str(tweets['text'])), location.latitude,location.longitude, loc]
						listOfLinks.append(statusLocList)

				except(AttributeError):
					pass

		return listOfLinks

	auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret) #using key from keys file - blank in github
	auth.set_access_token(keys.access_token, keys.access_secret)

	tweets = ""
	api = tweepy.API(auth)
	listOfLinks = []

	newdate = datetime.datetime.now() - datetime.timedelta(days=time)

	try:	#will be an error if the username is not valid

		for status in tweepy.Cursor(api.search, q=searchTerm).items(numTweets): 

			if (status.created_at > newdate): #filtering out dates that are not in right time period
				loc = str(status._json['user']['location'])
				if(loc != "None"):
					try:
						agent = "dataMining" + str(os.getpid())
						geolocator = Nominatim(user_agent=agent, timeout=3)
						location = geolocator.geocode(loc) #geocoding from received
						statusLocList = [get_tweet_sentiment(status.text), location.latitude,location.longitude, loc]
						listOfLinks.append(statusLocList)

					except(AttributeError):
						pass
		return listOfLinks # a success
	except (tweepy.TweepError):
		return [] #means the username was not valid!

def get_tweet_sentiment(tweetText): 

    custom_tokens = remove_noise(word_tokenize(tweetText))
    global classifier
    sentiment = classifier.classify(dict([token, True] for token in custom_tokens))
 #   print(sentiment)
    if (sentiment == "Positive"): 
    	return 1
    elif (sentiment == "Negative"):
    	return 3
    else:
    	return 2

def remove_noise(tweet_tokens, stop_words = ()): #removes noise aka removing @, retweeting people, links

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

def calibrate():
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    text = twitter_samples.strings('tweets.20150430-223406.json')
    tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]

    stop_words = stopwords.words('english')

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json') #files downloaded from setup.py used to calibrate the classifer for sentiment analysis
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    freq_dist_pos = FreqDist(all_pos_words)
    #print(freq_dist_pos.most_common(10))

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive") #calibrating positive
                         for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative") #calibrating negative
                         for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]
    global classifier

    classifier = NaiveBayesClassifier.train(train_data) #trains the data!
    print("Calibration complete!")

    print("Accuracy is:", classify.accuracy(classifier, test_data))

class StdOutListener(tweepy.StreamListener):
	def __init__(self, tweetCounter=0):
		self.tweetCounter = tweetCounter

	def on_data(self, data):
		JSONdata = json.loads(data)
		# if (JSONdata["coordinates"] != None):
		#     print(JSONdata["coordinates"])
		# print(JSONdata.get("user", {}).get("location", {}))
		try:
			loc = str(JSONdata.get("user", {}).get("location", {}))
			if(loc != "None"):
				agent = "dataMining" + str(os.getpid())
				geolocator = Nominatim(user_agent=agent, timeout=10)
				location = geolocator.geocode(loc)
				# sentimentList.append(get_tweet_sentiment(str(JSONdata.get("text", {}))))
				# coordsList.append(location.latitude)
				# coordsList.append(location.longitude)
				liveList.append([get_tweet_sentiment(str(JSONdata.get("text", {}))), location.latitude,location.longitude, loc])
				self.tweetCounter += 1
				if(self.tweetCounter == liveLimit):
					return False
				else:
					return True
		except(AttributeError):
			pass

	def on_error(self, status):
		print(status)