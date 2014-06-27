import urllib2
import json
import base64
import csv



def getIssues(baseURL,offset):
 	issuesURL = baseURL + "?offset=" + str(offset) + "&limit=100"
	response = urllib2.urlopen(issuesURL)
	data = json.load(response)
	return data["issues"]


def getContent(baseURL):
	print "Now scraping..."

	with open("guardianproject.csv", "wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
#		writer.writerow(["title", "text", "url", "tags"])

		offset = 0
		issues = getIssues(baseURL, offset)

		while len(issues) != 0:

			for issue in issues:
				body = issue['description']
				title = issue['subject']
				URL = "https://dev.guardianproject.info/issues/"+str(issue['id'])
				tag = issue['tracker']['name']+','+issue['project']['name']

				row = [unicode(title).encode("utf-8"), unicode(body).encode("utf-8"), URL, unicode(tag).encode("utf-8")]
				writer.writerow(row)

			offset = offset+100
			issues = getIssues(baseURL, offset)



getContent("https://dev.guardianproject.info/issues.json")
