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

moms = []
print 'Reading moms.txt...'
with open('moms.txt', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        if count == 0:
            count = 1
            continue
        mom = {}
        mom['screen_name'] = row[0]
        mom['desc'] = row[1]
        moms.append(mom)

tweets = []
print 'Grabbing tweets...'
for item in range(0, len(moms)):
    try:
        tweet = t.statuses.user_timeline(count=10, screen_name=moms[item]['screen_name'])
        tweets.append(tweet)
    except:
        pass


tweetChunks2 = []

print 'Combining tweets..'
for person in tweets:
    text = ""
    for tweets in person:
        text = text + tweets['text'] + ' '
    keywords = alchemy.keywords(text, 'json')
    tweet = {}
    tweet['chunk'] = text
    tweetChunks2.append(tweet)

fout = open('tweetChunks2.txt', 'wb')
writer = csv.writer(fout, delimiter='\t')
writer.writerow(['chunk', 'keyword'])
for item in range(0, len(tweetChunks2)):
	writer.writerow([tweetChunks2[item]['chunk']])

fout.close()
