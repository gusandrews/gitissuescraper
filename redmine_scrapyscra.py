import urllib2
import json
import base64
import csv



def getIssues(baseURL,offset):
 	issuesURL = baseURL + "?status_id=*?offset=" + str(offset) + "&limit=100"
	response = urllib2.urlopen(issuesURL)
	data = json.load(response)
	return data["issues"]

# keep only issues that are open or have been touched in last six months
def keepThisIssue(issue):
	if issue['status']['name'] != "Closed":
		print "Keeping open issue"
		return True

	from dateutil.parser import parse
	keepSince = parse("2014-01-01T12:00UTC")
	updatedAt = parse(issue['updated_on'])

	if updatedAt > keepSince:
		print "Keeping closed issue updated at " + issue['updated_on']

	return updatedAt > keepSince

def getContent(baseURL):
	print "Now scraping..."

	with open("guardianproject.csv", "wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
#		writer.writerow(["title", "text", "url", "tags"])

		offset = 0
		issues = getIssues(baseURL, offset)

		while len(issues) != 0:

			for issue in issues:
				if keepThisIssue(issue):
					body = unicode(issue['description'])
					title = unicode(issue['subject'])
					URL = "https://dev.guardianproject.info/issues/"+str(issue['id'])
					tag = ",".join(["tracker:"+issue['tracker']['name'], 
						  			"project:"+issue['project']['name'],
						  			"statusName:"+issue['status']['name']])

					row = [unicode(title).encode("utf-8"), unicode(body).encode("utf-8"), URL, unicode(tag).encode("utf-8")]
					writer.writerow(row)

			offset = offset+100
			issues = getIssues(baseURL, offset)



getContent("https://dev.guardianproject.info/issues.json")
