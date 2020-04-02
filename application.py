import sys
from flask import Flask, render_template, request, send_file
import os
import searchTerms

application = Flask(__name__)

@application.route('/') #creates the flask html route
def root():
    return render_template('main.html')

@application.route('/', methods=['POST']) #creates the flask html route
def post():
	searchTerm = request.form['searchTerm'] #getting usernames
	print(searchTerm)
	timeStr = request.form['time'] #getting time period
	time = 0
	if (timeStr == "day"): 
		time = 1
	elif(timeStr == "month"): 
		time = 30
	elif(timeStr == "year"): 
		time = 365
	print(time)
	terms = searchTerms.startUp(searchTerm, time)
#	print('Terms ', terms)
	return render_template('main.html')


if __name__ == '__main__':
	application.run()
#    application.run(host = '0.0.0.0', port = 8080) for aws