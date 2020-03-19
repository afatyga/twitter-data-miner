import keys #holds the keys for using tweepy
import tweepy #twitter api
from threading import Thread #threading stuff
from geopy.geocoders import Nominatim

numTweets = 1000

def getMsgs(searchTerm):
	if not isinstance(searchTerm,str): #can only take in a string
		return []

	if (keys.consumer_key == ""): #meaning all are empty => should read backupTweets.json!

		listOfLinks  = []
		with open('backupTweets.json') as json_file:
		    data = json.load(json_file)
		    for tweets in data['tweets']:
		    	listOfLinks.append((str(tweets['text']),0))

		return listOfLinks

	auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret) #using key from keys file - blank in github
	auth.set_access_token(keys.access_token, keys.access_secret)

	tweets = ""
	api = tweepy.API(auth)
	listOfLinks = []

	try:	#will be an error if the username is not valid

		for status in tweepy.Cursor(api.search, q=searchTerm).items(10): 

			loc = str(status._json['user']['location'])
			try:
				geolocator = Nominatim(user_agent="Data Mining")
				location = geolocator.geocode(loc)
				
				statusLocList = [status.text, location.latitude,location.longitude]
				listOfLinks.append(statusLocList)

			except(AttributeError):
				pass

		return listOfLinks # a success
	except (tweepy.TweepError):
		return [] #means the username was not valid!

def startUp(searchTerm): 

	geoLocList = getMsgs(searchTerm) 
	return geoLocList

startUp("dog")
