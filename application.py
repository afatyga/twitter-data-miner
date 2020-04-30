import sys
from flask import Flask, render_template, request, send_file
import os
import searchTerms
import xlsxwriter
import json
import zipfile

global cords
cords = []
global cords2
cords2 = []

global sentiment, sentiment2
sentiment = []
sentiment2 = []

global nextCords2Use
nextCords2Use = 2

global search1, search2
search1 = ""
search2 = ""

application = Flask(__name__)

@application.route('/') #creates the flask html route
def root():
	os.system("del /q Export\*")#windows
	os.system("rm  Export/*")    #mac/linux
	os.system("rm data.zip")
	os.system("del data.zip")
	searchTerms.calibrate()
	return render_template('main.html', butOn = 0, loc_cords = [], loc_cords2 = [], search1 ="", search2 ="",)

@application.route('/', methods=['POST']) #creates the flask html route
def post():

	if request.form['action'] == 'Search':

		global cords, cords2
		global sentiment, sentiment2, nextCords2Use, search1, search2

		searchTerm = request.form['searchTerm'] #getting usernames
		timeStr = request.form.get('time') #getting time period
		print(timeStr)
		overlay = request.form.get('overlay')

		print(overlay)
		if (overlay == None): 
			cords = []
			cords2 = []
			sentiment = []
			sentiment2 = []
			search1 = ""
			search2 = ""

		#path
		reportName = "Export/" + str(searchTerm) + "_" + str(timeStr) + ".xlsx"

		# Create a workbook and add a worksheet.
		workbook = xlsxwriter.Workbook(reportName)
		worksheet = workbook.add_worksheet()
		worksheet.write(0, 0, 'Area')
		worksheet.write(0, 1, 'Sentiment')

		time = 0
		terms = []

		if (timeStr == "day"): 
			time = 1
			terms = searchTerms.getMsgs(searchTerm, time)
		elif(timeStr == "month"): 
			time = 30
			terms = searchTerms.getMsgs(searchTerm, time)
		elif(timeStr == "year"):
			time = 365
			terms = searchTerms.getMsgs(searchTerm, time)
		elif(timeStr == "live"): #justin here is where you call the function 
			print("AH")

		rowNum = 1

		tempCords = []
		tempSent = []

		for t in terms: #adding to excel file
			tempCords.append(float(t[1]))
			tempCords.append(float(t[2]))
			tempSent.append(t[0])

			sentimentStr = ""
			if (t[0] == 1): sentimentStr = "positive"
			if (t[0] == 2): sentimentStr = "neutral"
			if (t[0] == 3): sentimentStr = "negative"
			worksheet.write(rowNum, 0, t[3])
			worksheet.write(rowNum, 1, sentimentStr)
			rowNum = rowNum + 1

		if(overlay == None):
			cords = tempCords
			sentiment = tempSent
			search1 = searchTerm
			cords2 = []
			sentiment2 = []
			search2 = ""
		elif (cords == [] and cords2 == []): 
			cords = tempCords
			sentiment = tempSent
			search1 = searchTerm
			nextCords2Use = 2
		elif(cords2 == []):
			cords2 = tempCords
			sentiment2 = tempSent
			search2 = searchTerm
			nextCords2Use = 1
		elif(nextCords2Use == 1):
			cords = tempCords
			sentiment = tempSent
			search1 = searchTerm
			nextCords2Use = 2
		elif(nextCords2Use == 2):
			cords2 = tempCords
			sentiment2 = tempSent
			search1 = searchTerm
			nextCords2Use = 1

		workbook.close() #closing excel file

		return render_template('main.html', butOn = 1, loc_cords = (cords), loc_cords2 = (cords2), sent_list = (sentiment), sent_list2 = (sentiment2), search1 = search1, search2 = search2,)

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