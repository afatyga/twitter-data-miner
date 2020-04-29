# Final Project - Alex Fatyga, Noah Malhi, Justin Morgan

Our twitter data mining project will essentially have a user input a search term for twitter and display a map of the US and point out what regions find this search term positive, negative or don't have enough data to backup a decision. We will be utilizing a Flask web application and AWS to host it on the cloud.

# User Stories
Companies want to see how the US views their brand. They may want to compare opinions from the past year to the past 6 months to the past month to see how opinions have changed.

# How To Use It
- In terminal, run pip3 install -r requirements.txt
- Put in Twitter keys in keys.py
- For first run, run python3 setup.py
- Then run python3 application.py
- Go into your web browser and go onto 127.0.0.1:5000

# How Did We Do It?
We started by making a python script using Tweepy that can take in a search term and return a list of tweets then we looked into getting the location of these tweets. The status and location (longitude and latitude) were grouped together into a list of lists that then could undergo sentiment analysis. After this simple python script was started, we then created a simple web application so that we can enter a location on the web app. Then we added in a drop down list so users can ask for the last day, 30 days, year or live update of tweets to be searched through and sent this to the python script so it could filter out tweets that were too old. 

## Front End Requests

## Sentiment Analysis

## Data Grouping

## Data Overlaying

## Twitter Live Streaming

# Completed Work
Basic Web App to allow users to input a search term and decide how far back twitter will go (past day, past 30 days, past year). Sentiment analysis is run on these tweets and the latitude and longitude is determined using geolocation. Users can also export an excel file of this data. Separately, we were able to create a map that groups data points together with various different colored markers. Our next step is to put these 2 parts together.

# Roles
- Alex => making tweepy api request, geocoding, export output into an excel spreadsheet, improved sentiment analysis, front end view
- Justin => Sentiment analysis, live tweepy streaming
- Noah => Placing data points onto the map, grouping these data points together, data overlaying, front end map

# Sources
https://www.datacamp.com/community/tutorials/simplifying-sentiment-analysis-python
