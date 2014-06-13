# For (URL of repo)
# grab json
# For (issues)
# 	For (comments)
#		Create comment string
#		get comment number
#				Get comment text for comment number
#				Add to string
#				get next comment
# Write string


import urllib2
import json
import base64
import csv


def getJsonWithAuth(url):
	username = ''
	password = ''
	
	request = urllib2.Request(url)
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string) 

	result = urllib2.urlopen(request)
	return json.load(result)
	

def getContent(owner,repo):
	
	issuesURL = "https://api.github.com/repos/"+owner+"/"+repo+"/issues?per_page=100"
	# Note we may need to go back and iterate over pages in order to get >100 issues

	print "Now scraping "+issuesURL+"..."

	data = getJsonWithAuth(issuesURL)


	with open(owner+"_"+repo+".csv", "wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		writer.writerow(["title", "text", "url", "tags"])
		for issue in data:
			body = issue['body']
			title = issue['title']
			commentsURL = issue['comments_url']
			commentsdata = getJsonWithAuth(commentsURL)	
	
			for comment in commentsdata:
				body = body+"\n"+comment['body']

			labelNames = ','.join(x['name'] for x in issue['labels'])	
			row = [unicode(title).encode("utf-8"), unicode(body).encode("utf-8"), issue['url'], labelNames]
			writer.writerow(row)

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
	[ "opentechinstitute", ["commotion-router","commotion-docs","luci-theme-commotion","commotiond","commotion-client"]],
	[ "WhisperSystems", ["TextSecure", "TextSecure-Browser", "TextSecure-iOS", "RedPhone"]]
]	

for project in allProjects:
	owner = project[0]
	repos = project[1]
	for repo in repos:
		getContent(owner,repo)
		