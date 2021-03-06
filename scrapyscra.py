# Github issue scraper. 
# Saves each repo's issues as a CSV with columns text, title, URL, tags
# tags are issue labels, plus repo and project names, comma separated
# Hard-coded repo list below, no command line args

import urllib2
import json
import base64
import csv

def getJsonWithAuth(url):
	username = 'gusandrews'
	password = ''

	request = urllib2.Request(url)
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)

	result = urllib2.urlopen(request)
	return json.load(result)


def buildURL(owner,repo,pageOffset):
	pageSize = 100
	return "https://api.github.com/repos/"+owner+"/"+repo+"/issues?state=all&page="+str(pageOffset)+"&per_page="+str(pageSize)


# keep only issues that are open or have been touched in last six months
def keepThisIssue(issue):
	if issue['state'] == "open":
		print "Keeping open issue"
		return True

	from dateutil.parser import parse
	keepSince = parse("2014-01-01T12:00UTC")
	updatedAt = parse(issue['updated_at'])

	if updatedAt > keepSince:
		print "Keeping closed issue updated at " + issue['updated_at']

	return updatedAt > keepSince


def getContent(owner,repo):
	pageOffset = 1
	issuesURL = buildURL(owner,repo,pageOffset)
	print "Now scraping "+issuesURL+"..."
	data = getJsonWithAuth(issuesURL)

	with open(owner+"_"+repo+".csv", "wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
#		writer.writerow(["title", "text", "url", "tags"])

		while len(data) != 0:

			for issue in data:

				if keepThisIssue(issue):
					body = unicode(issue['body'])
					title = unicode(issue['title'])
					commentsURL = issue['comments_url']
					commentsdata = getJsonWithAuth(commentsURL)

					for comment in commentsdata:
						body = body+"\n"+unicode(comment['body'])

					labelNames = ','.join(["label:"+x['name'] for x in issue['labels']] + 
										  ["owner:"+owner, "repo:"+repo, "state:"+issue['state']])

					row = [unicode(title).encode("utf-8"), unicode(body).encode("utf-8"), issue['url'], labelNames]
					writer.writerow(row)

			pageOffset=pageOffset+1
			issuesURL = buildURL(owner,repo,pageOffset)
			print "Now scraping "+issuesURL+"..."
			data = getJsonWithAuth(issuesURL)


allProjects = [
	[ "cryptocat", ["cryptocat","cryptocat-ios","cryptocat-android"]],
	[ "servalproject", ["batphone"]],
	[ "chrisballinger", ["ChatSecure-iOS"]],
	[ "getlantern", ["www.getlantern.org", "lantern"]],
	[ "toberndo", ["mailvelope"]],
	[ "jitsi", ["jitsi-meet"]],
	[ "glamrock", ["cupcake"]],
	[ "benetech", ["martus-android"]],
	[ "byzantium", ["byzantium"]],
	[ "opentechinstitute", ["commotion-router","commotion-docs","luci-commotion","commotiond","commotion-client"]],
	[ "WhisperSystems", ["TextSecure", "TextSecure-Browser", "TextSecure-iOS", "RedPhone"]]
]


for project in allProjects:
	owner = project[0]
	repos = project[1]
	for repo in repos:
		getContent(owner,repo)
