import sys
from flask import Flask, render_template, request, send_file
import os
import searchTerms
import xlsxwriter
import json
import zipfile

application = Flask(__name__)

@application.route('/') #creates the flask html route
def root():
	os.system("del /q Export\*")#windows
	os.system("rm  Export/*")    #mac/linux
	return render_template('main.html', butOn = 0, loc_cords = [])

@application.route('/', methods=['POST']) #creates the flask html route
def post():

	
	if request.form['action'] == 'Search':
		searchTerm = request.form['searchTerm'] #getting usernames
		print(searchTerm)
		timeStr = request.form['time'] #getting time period


		global reportName
		reportName = "Export/" + str(searchTerm) + "_" + str(timeStr) + ".xlsx"

		# Create a workbook and add a worksheet.
		workbook = xlsxwriter.Workbook(reportName)
		worksheet = workbook.add_worksheet()
		worksheet.write(0, 0, 'Area')
		worksheet.write(0, 1, 'Sentiment')

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
			cords.append(float(t[1]))
			cords.append(float(t[2]))
			sentiment.append(t[0])
			worksheet.write(rowNum, 0, t[3])
			worksheet.write(rowNum, 1, t[0])
			rowNum = rowNum + 1
			workbook.close() #closing excel file
		
		
		print(cords)
		return render_template('main.html', butOn = 1, loc_cords = (cords), sent_list = (sentiment),)

	if request.form['action'] == 'Export':
		zipFolder = zipfile.ZipFile('data.zip','w', zipfile.ZIP_DEFLATED) #making the zip and sending it to the user!!!
		for root, directs, files in os.walk('Export/'):
			for f in files:
				zipFolder.write('Export/' + str(f))
		zipFolder.close()
		return send_file('data.zip', mimetype ='zip', attachment_filename = 'data.zip', as_attachment=True)


if __name__ == '__main__':
	application.run()
#    application.run(host = '0.0.0.0', port = 8080) for aws