import sys
from flask import Flask, render_template, request, send_file
import os	#executes os commands to delete files
import searchTerms # file to execute tweepy requests and sentiment analysis
import xlsxwriter # for export - to write the excel file
import zipfile #for export -  to zip the excel files together

# the following global variables are for data overlaying
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

application = Flask(__name__) #for flask

@application.route('/') #creates the flask html route
def root():	#delete zip file and excel files
	os.system("del /q Export\*")#windows
	os.system("rm  Export/*")    #mac/linux
	os.system("rm data.zip")
	os.system("del data.zip")

	searchTerms.calibrate()
	return render_template('main.html', butOn = 0, loc_cords = [], loc_cords2 = [], terms_list = ["",""],)

@application.route('/', methods=['POST']) #creates the flask html route upon button clicks
def post():

	if request.form['action'] == 'Search': #for search button

		global cords, cords2
		global sentiment, sentiment2, nextCords2Use, search1, search2

		searchTerm = request.form['searchTerm'] #getting search term
		timeStr = request.form.get('time') #getting time period
		print(timeStr)
		overlay = request.form.get('overlay') #whether they want an overlay or not
		print(overlay)
		if (overlay == None): #resets everything if they don't want an overlay
			cords = []
			cords2 = []
			sentiment = []
			sentiment2 = []
			search = []

		#path for excel file
		reportName = "Export/" + str(searchTerm) + "_" + str(timeStr) + ".xlsx"

		# Create a workbook and add a worksheet
		workbook = xlsxwriter.Workbook(reportName)
		worksheet = workbook.add_worksheet()
		worksheet.write(0, 0, 'Area') # first row
		worksheet.write(0, 1, 'Sentiment')

		time = 0 # for actual time
		terms = []

		if (timeStr == "day"): #setting the time and running correct function based on timeStr 
			time = 1
			terms = searchTerms.getMsgs(searchTerm, time)
		elif(timeStr == "month"): 
			time = 30
			terms = searchTerms.getMsgs(searchTerm, time)
		elif(timeStr == "year"):
			time = 365
			terms = searchTerms.getMsgs(searchTerm, time)
		elif(timeStr == "live"): #justin here is where you call the function 
			terms = searchTerms.getLiveMsgs(searchTerm)

		rowNum = 1

		# temporary variables until placed into correct variable (necessary for overlaying)
		tempCords = []
		tempSent = []

		for t in terms: #adding to excel file, setting sentimentstr to add to excel, getting proper temp variables
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


		# the following sets the correct variables for overlaying or not overlaying to send to front end
		if(overlay == None):
			cords = tempCords
			sentiment = tempSent
			search1 = searchTerm
			cords2 = [] #resetting
			sentiment2 = []
			search2 = ""
		elif (cords == [] and cords2 == []): #both empty, default to 1 
			cords = tempCords
			sentiment = tempSent
			search1 = searchTerm
			nextCords2Use = 2
		elif(cords2 == []): #second empty, default to 1
			cords2 = tempCords
			sentiment2 = tempSent
			search2 = searchTerm
			nextCords2Use = 1
		elif(nextCords2Use == 1): #next is 1 so set 1
			cords = tempCords
			sentiment = tempSent
			search1 = searchTerm
			nextCords2Use = 2
		elif(nextCords2Use == 2): #next to 2 so set 2
			cords2 = tempCords
			sentiment2 = tempSent
			search1 = searchTerm
			nextCords2Use = 1

		workbook.close() #closing excel file

		print(cords)
		print(cords2)
		#list to hold search terms
		search = []
		search.append(search1)
		search.append(search2)
		return render_template('main.html', butOn = 1, loc_cords = (cords), loc_cords2 = (cords2), sent_list = (sentiment), sent_list2 = (sentiment2), terms_list = (search),)

	if request.form['action'] == 'Export': #for when export is pressed, send a zip file of all the excel files in the Export folder
		zipFolder = zipfile.ZipFile('data.zip','w', zipfile.ZIP_DEFLATED) #making the zip and sending it to the user!!!
		for root, directs, files in os.walk('Export/'):
			for f in files:
				zipFolder.write('Export/' + str(f))
		zipFolder.close()
		return send_file('data.zip', mimetype ='zip', attachment_filename = 'data.zip', as_attachment=True)

if __name__ == '__main__':
	application.run()