# Needs authentication for pagination probably. As of now it works though.
# ADD the Enigmail tracker http://sourceforge.net/p/enigmail/bugs/
# Also they have a forum! http://sourceforge.net/p/enigmail/forum/

import urllib2
import json
import base64
import csv

def getIssueList(baseURL,page):
	response = urllib2.urlopen(baseURL + "?page=" + str(page))
	data = json.load(response)
	return data["tickets"]

def getIssueContent(ticketURL):
	response = urllib2.urlopen(ticketURL)
	data = json.load(response)
	return data["ticket"]

# keep only issues that are open or have been touched in last six months
def keepThisIssue(issue):
	if issue['status'] == "open":
		print "Keeping open issue"
		return True

	from dateutil.parser import parse
	keepSince = parse("2014-01-01")
	updatedAt = parse(issue['mod_date'])

	if updatedAt > keepSince:
		print "Keeping closed issue updated at " + issue['mod_date']

	return updatedAt > keepSince

# scrape issues. Usually /bugs, but also /support-requests and /feature-requests use this format
def getIssues(projectName, issueType):
	baseURL = "http://sourceforge.net/rest/p/" + projectName + "/" + issueType
	print "Retrieving " + baseURL + "..."

	pageNum = 0 # sourceForge starts paging at 0
	issues = getIssueList(baseURL,pageNum)

	with open(projectName + "-" + issueType + ".csv", "wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		#writer.writerow(["title", "text", "url", "tags"])

		# page loop
		while len(issues) != 0:

			for issue in issues:
				ticketNumber = issue['ticket_num']
				ticketURL = baseURL + "/" + str(ticketNumber)
				content = getIssueContent(ticketURL)

				if keepThisIssue(content):
					body = unicode(content['description'])
					title = unicode(content['summary'])
					URL = ticketURL
					tag = ','.join(["label:"+x for x in content['labels']] + 
								   ["project:"+projectName, "postType:"+issueType, "status:"+content['status']])

					# add each discussion post into the text of the issue
					discussion = content['discussion_thread']['posts']
					for post in discussion:
						body = body+"\n---------------\n"+post['text']
						#print post['text']

					row = [unicode(title).encode("utf-8"), unicode(body).encode("utf-8"), URL, tag]
					writer.writerow(row)

			pageNum += 1
			issues = getIssueList(baseURL,pageNum)




def getThreadList(baseURL,page):
	response = urllib2.urlopen(baseURL + "?page=" + str(page))
	data = json.load(response)
	return data["forum"]["topics"]

def getThreadContent(threadURL):
	response = urllib2.urlopen(threadURL)
	data = json.load(response)
	return data["topic"]["posts"]

# scrape all threads in a forum
def getThreads(projectName, forumName):
	baseURL = "http://sourceforge.net/rest/p/" + projectName + "/forum/" + forumName
	print "Retrieving " + baseURL + "..."

	pageNum = 0 # sourceForge starts paging at 0
	threads = getThreadList(baseURL,pageNum)

	with open(projectName + "-" + forumName + ".csv", "wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		#writer.writerow(["title", "text", "url", "tags"])

		# page loop
		while len(threads) != 0:

			for thread in threads:
				threadID = thread['_id']
				threadURL = baseURL + "/thread/" + str(threadID)
				print "Found thread " + threadURL
				content = getThreadContent(threadURL)

				title = thread["subject"]
				URL = threadURL
				tag = ','.join(["project:"+projectName, "postType:"+forumName])

				# join all posts together
				body = "\n---------------\n".join([x["text"] for x in content])

				row = [unicode(title).encode("utf-8"), unicode(body).encode("utf-8"), URL, tag]
				writer.writerow(row)

			pageNum += 1
			threads = getThreadList(baseURL,pageNum)

getIssues("keepass", "bugs")
getIssues("keepass", "support-requests")
getIssues("keepass", "feature-requests")
getIssues("enigmail", "bugs")
getThreads("enigmail", "support")
getThreads("enigmail", "feature_requests")
