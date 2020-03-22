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
	terms = searchTerms.getMsgs(searchTerm)
	print('Terms ', terms)
	return render_template('main.html')


if __name__ == '__main__':
	application.run()
#    application.run(host = '0.0.0.0', port = 8080)