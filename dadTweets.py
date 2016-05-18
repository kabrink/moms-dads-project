import twitter
import oauthDance
import json
import csv
from time import sleep
import re
import sys
from alchemyapi import AlchemyAPI


alchemy = AlchemyAPI()

reload(sys)
sys.setdefaultencoding('utf-8')

t = oauthDance.login()

count = 0

dads = []

#print 'Reading dads.txt...'
reader = csv.reader(open('dads-update.txt', 'rU'), dialect=csv.excel_tab)
for row in reader:
    if count == 0:
        count = 1
        continue
    dad = {}
    dad['screen_name'] = row[0]
    dad['desc'] = row[1]
    dads.append(dad)


tweets = []
#print 'Grabbing tweets...'
for item in range(0, len(dads)):
    try:
        tweet = t.statuses.user_timeline(count=10, screen_name=dads[item]['screen_name'])
        tweets.append(tweet)
    except:
        pass

#print tweets
print len(tweets)
tweetText = []

for tweetResponse in tweets:
    for tweet in tweetResponse:
        tweetText.append(tweet['text'])

#==============================================================================
# fout = open('tweets2.txt', 'wb')
# writer = csv.writer(fout, delimiter='\t')
# for tweetResponse in tweets:
#     for tweet in tweetResponse:
#          writer.writerow(tweet['text'].encode('ascii', 'ignore'))
# fout.close()
#==============================================================================


#tweets = []
# with open('tweetChunks.txt', 'rb') as csvfile:
#     reader = csv.reader(csvfile, delimiter='\t')
#     for row in reader:
#         if count == 0:
#             count = 1
#             continue
#         tweet = row[0]
#         tweets.append(tweet)

#print tweets

tweetChunks = []

print 'Combining tweets..'
allText = ''
for i in range(0,len(tweetText)/10):
    text = ''
    for j in range(0,10):
        currentText = tweetText[(10*i)+j]
        noRtText = re.sub(r'\bRT\b'," ", currentText)
        noUrlText = re.sub(r"http\S+","", noRtText)
        text = text + noUrlText + ' '
        allText = allText + noUrlText + ' '
    keywords = alchemy.keywords('text', text)
    sentiment = alchemy.sentiment('text',text)
    tweet = {}
    tweet['chunk'] = text
    tweet['keywords'] = ''
    tweet['sentiment'] = sentiment['docSentiment']['type'] + ' ' + sentiment['docSentiment']['score'] + ' '
    for word in keywords['keywords']:
        tweet['keywords'] = tweet['keywords'] + word['text'] + ' ' + word['relevance'] + ' '
    tweetChunks.append(tweet)

overallResult = {}
overallResult['chunk'] = allText
keywords = alchemy.keywords('text', allText)
overallResult['keywords'] = ''
sentimentType = alchemy.sentiment('text',allText)['docSentiment']['type']
sentimentScore = alchemy.sentiment('text',allText)['docSentiment']['score']
overallResult['sentiment'] = sentimentType + ' ' + sentimentScore + ' ' 
for word in keywords['keywords']:
    overallResult['keywords'] = overallResult['keywords'] + word['text'] + ' ' + word['relevance'] + ' '


print '\n\n\n'
print tweetChunks[0]['chunk']
print '\n'
print tweetChunks[0]['keywords']
print '\n\n\n'

fout = open('tweetChunks2.txt', 'wb')
writer = csv.writer(fout, delimiter='\t')
writer.writerow(['chunk', 'keyword'])
for item in range(0, len(tweetChunks)):
	writer.writerow([tweetChunks[item]['chunk'], tweetChunks[item]['keywords'], tweetChunks[item]['sentiment']])
writer.writerow([overallResult['chunk'], overallResult['keywords'], overallResult['sentiment']])
fout.close()
