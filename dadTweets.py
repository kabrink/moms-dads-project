import twitter
import oauthDance
import json
import csv
from time import sleep
import sys
from alchemyapi import AlchemyAPI


alchemy = AlchemyAPI()

reload(sys)
sys.setdefaultencoding('utf-8')

t = oauthDance.login()

count = 0

dads = []

print 'Reading dads.txt...'
with open('dads.txt', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        if count == 0:
            count = 1
            continue
        dad = {}
        dad['screen_name'] = row[0]
        dad['desc'] = row[1]
        dads.append(dad)

tweets = []
print 'Grabbing tweets...'
for item in range(0, len(dads)):
    try:
        tweet = t.statuses.user_timeline(count=10, screen_name=dads[item]['screen_name'])
        tweets.append(tweet)
    except:
        pass

tweetChunks = []

print 'Combining tweets..'
for person in tweets:
    text = ""
    for tweets in person:
        text = text + tweets['text'] + ' '
    keywords = alchemy.keywords(text, 'json')
    tweet = {}
    tweet['chunk'] = text
    tweet['keywords'] = ''
    for word in keywords['keywords']:
        tweet['keywords'] = tweet['keywords'] + word['text']
    tweetChunks.append(tweet)

fout = open('tweetChunks.txt', 'wb')
writer = csv.writer(fout, delimiter='\t')
writer.writerow(['chunk', 'keyword'])
for item in range(0, len(tweetChunks)):
	writer.writerow([tweetChunks[item]['chunk'], tweetChunks[item]['keywords']])

fout.close()
