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


def getJsonWithAuth(url):
	username = ''
	password = ''
	
	request = urllib2.Request(url)
	base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string) 

	result = urllib2.urlopen(request)
	return json.load(result)
	
	
issuesURL = "https://api.github.com/repos/cryptocat/cryptocat/issues?per_page=100"
# Note we may need to go back and iterate over pages in order to get >100 issues

data = getJsonWithAuth(issuesURL)

for issue in data:
	print issue['body']
	print issue['comments_url']
	commentsURL = issue['comments_url']

	commentsdata = getJsonWithAuth(commentsURL)	
	
	for comment in commentsdata:
		print "OHAI COMMENT"
		print comment['body']

