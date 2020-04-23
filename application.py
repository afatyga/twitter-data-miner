import sys
from flask import Flask, render_template, request, send_file
import os
import searchTerms
import xlsxwriter
import json

application = Flask(__name__)

@application.route('/') #creates the flask html route
def root():
    return render_template('main.html', butOn = 0)

@application.route('/', methods=['POST']) #creates the flask html route
def post():

	
	if request.form['action'] == 'Search':
		searchTerm = request.form['searchTerm'] #getting usernames
		print(searchTerm)

		global reportName
		reportName = str(searchTerm) + ".xlsx"

		# Create a workbook and add a worksheet.
		workbook = xlsxwriter.Workbook(reportName)
		worksheet = workbook.add_worksheet()
		worksheet.write(0, 0, 'Area')
		worksheet.write(0, 1, 'Sentiment')

		timeStr = request.form['time'] #getting time period
		time = 0
		if (timeStr == "day"): 
			time = 1
		elif(timeStr == "month"): 
			time = 30
		elif(timeStr == "year"): 
			time = 365
#		print(time)

		terms = searchTerms.getMsgs(searchTerm, time)
		
		cords = []
		sentiment = []
		rowNum = 1
		for t in terms: #adding to excel file
			cords.append(t[1])
			cords.append(t[2])
			sentiment.append(t[0])
			worksheet.write(rowNum, 0, t[3])
			worksheet.write(rowNum, 1, t[0])
			rowNum = rowNum + 1
			workbook.close() #closing excel file
		
		
		print(cords)
		return render_template('main.html', butOn = 1, loc_cords = json.dumps(cords), sent_list = json.dumps(sentiment),)

	if request.form['action'] == 'Export':
		
		return send_file(reportName, mimetype ='application/vnd.ms-excel', attachment_filename = reportName, as_attachment=True)



if __name__ == '__main__':
	application.run()
#    application.run(host = '0.0.0.0', port = 8080) for aws