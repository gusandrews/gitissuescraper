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

def getIssueList(baseURL):
response = urllib2.urlopen(baseURL)
data = json.load(response)
return data["tickets"]

def getIssueContent(ticketURL):
response = urllib2.urlopen(ticketURL)
data = json.load(response)
return data["ticket"]

def getContent(baseURL):

issues = getIssueList(baseURL)

with open("keepass.csv", "wb") as csv_file:
writer = csv.writer(csv_file, delimiter=',')
writer.writerow(["title", "text", "url", "tags"])

for issue in issues:
ticketNumber = issue['ticket_num']
ticketURL = baseURL + str(ticketNumber)

print "Now scraping..." + ticketURL

content = getIssueContent(ticketURL)

body = content['description']
title = content['summary']
URL = ticketURL
tag = ','.join(content['labels'])

discussion = content['discussion_thread']['posts']

for post in discussion:
body = body+"\n"+post['text']
print post['text']

row = [unicode(title).encode("utf-8"), unicode(body).encode("utf-8"), URL, tag]
writer.writerow(row)


getContent("http://sourceforge.net/rest/p/keepass/bugs/")