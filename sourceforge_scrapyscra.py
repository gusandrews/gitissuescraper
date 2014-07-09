# Needs authentication for pagination probably. As of now it works though.
# ADD the Enigmail tracker http://sourceforge.net/p/enigmail/bugs/
# Also they have a forum! http://sourceforge.net/p/enigmail/forum/

import urllib2
import json
import base64
import csv

def getJsonWithAuth(url):
	BEARER_TOKEN = ''
	# this isn't done

def getIssueList(baseURL,page):
	response = urllib2.urlopen(baseURL + "?page=" + str(page))
	data = json.load(response)
	return data["tickets"]

def getIssueContent(ticketURL):
	response = urllib2.urlopen(ticketURL)
	data = json.load(response)
	return data["ticket"]

def getContent(projectName):
	baseURL = "http://sourceforge.net/rest/p/" + projectName + "/bugs/"
	print "Retrieving " + baseURL + "..."

	pageNum = 0 # sourceForge starts paging at 0
	issues = getIssueList(baseURL,pageNum)

	with open(projectName + ".csv", "wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		#writer.writerow(["title", "text", "url", "tags"])

		# page loop
		while len(issues) != 0:

			for issue in issues:
				ticketNumber = issue['ticket_num']
				ticketURL = baseURL + str(ticketNumber)
				content = getIssueContent(ticketURL)

				if content['status'] == "open":
					print "Found open issue " + ticketURL
					body = content['description']
					title = content['summary']
					URL = ticketURL
					tag = ','.join(content['labels'])

					# add each discussion post into the text of the issue
					discussion = content['discussion_thread']['posts']
					for post in discussion:
						body = body+"\n-------\n"+post['text']
						#print post['text']

					row = [unicode(title).encode("utf-8"), unicode(body).encode("utf-8"), URL, tag]
					writer.writerow(row)

			pageNum += 1
			issues = getIssueList(baseURL,pageNum)


getContent("keepass")
getContent("enigmail")
