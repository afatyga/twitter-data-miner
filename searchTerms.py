import keys #holds the keys for using tweepy
import tweepy #twitter api
from threading import Thread #threading stuff
from geopy.geocoders import Nominatim

numTweets = 30
import datetime
# datetime object containing current date and time


def getMsgs(searchTerm, time):
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

	newdate = datetime.datetime.now()
	if (time == 1): newdate = datetime.datetime.now() - datetime.timedelta(days=1)
	if (time == 30): newdate = datetime.datetime.now() - datetime.timedelta(days=30)
	if (time == 365): newdate = datetime.datetime.now() - datetime.timedelta(days=365)

	try:	#will be an error if the username is not valid

		for status in tweepy.Cursor(api.search, q=searchTerm).items(numTweets): 
#			print(now)
#			print(status.created_at)
#			print(abs(status.created_at - now))


			if (status.created_at > newdate):
				loc = str(status._json['user']['location'])
		#	listOfLinks.append([status.text, ])
				try:
					geolocator = Nominatim(user_agent="Data Mining1")
					location = geolocator.geocode(loc)
				
					statusLocList = [status.text, location.latitude,location.longitude]
					listOfLinks.append(statusLocList)

				except(AttributeError):
					pass

		print(len(listOfLinks))
		return listOfLinks # a success
	except (tweepy.TweepError):
		return [] #means the username was not valid!

def startUp(searchTerm, time): 

	geoLocList = getMsgs(searchTerm, time) 
	return geoLocList

