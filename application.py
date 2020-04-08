import sys
from flask import Flask, render_template, request, send_file
import os
import searchTerms
import xlsxwriter

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('report.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write(0, 0, 'Area')
worksheet.write(0, 1, 'Sentiment')



application = Flask(__name__)

@application.route('/') #creates the flask html route
def root():
    return render_template('main.html', butOn = 0)

@application.route('/', methods=['POST']) #creates the flask html route
def post():
	if request.form['action'] == 'Search':
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

		print('Terms ', terms)
		return render_template('main.html', butOn = 1)

	elif request.form['action'] == 'Export':
		workbook.close()
		return send_file('report.xlsx', mimetype ='application/vnd.ms-excel', attachment_filename = 'report.xlsx', as_attachment=True)

		#return render_template('main.html', butOn = 1)



if __name__ == '__main__':
	application.run()
#    application.run(host = '0.0.0.0', port = 8080) for aws