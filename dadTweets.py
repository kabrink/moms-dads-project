import csv
import json
import oauthDance
import re
import sys
import twitter
from alchemyapi import AlchemyAPI
from time import sleep

# Initialize Alchemy and Twitter communications
alchemy = AlchemyAPI()
reload(sys)
sys.setdefaultencoding('utf-8')
t = oauthDance.login()
count = 0

#empty list for dads
dads = []
reader = csv.reader(open('dads-update.txt', 'rU'), dialect=csv.excel_tab)
for row in reader:
    #skip header row
    if count == 0:
        count = 1
        continue

    dad = {}
    dad['screen_name'] = row[0]
    dad['desc'] = row[1]
    dads.append(dad)

# For every dad, grab 10 latest tweets
tweets = []
for item in range(0, len(dads)):
    try:
        tweetResponse = t.statuses.user_timeline(count=10, screen_name=dads[item]['screen_name'])
        tweets.append(tweetResponse)
    except:
        pass

tweetText = []

# Turn data into a list of the tweet text
for tweetResponse in tweets:
    for tweet in tweetResponse:
        tweetText.append(tweet['text'])

# Split list of tweet text into tweet chunks and do analysis
tweetChunks = []
allText = ''
# analyze each tweetChunk
for i in range(0,len(tweetText)/10):
    text = ''
    for j in range(0,10):
        currentText = tweetText[(10*i)+j]
        # Use regular expressions to remove 'RT' and urls
        noRtText = re.sub(r'\bRT\b'," ", currentText)
        noUrlText = re.sub(r"http\S+","", noRtText)
        text = text + noUrlText + ' '
        allText = allText + noUrlText + ' '
    # Call AlchemyAPI to get keywords and sentiment from current tweetChunk
    keywords = alchemy.keywords('text', text)
    sentiment = alchemy.sentiment('text',text)
    tweet = {}
    tweet['chunk'] = text
    tweet['keywords'] = ''
    tweet['sentiment'] = sentiment['docSentiment']['type'] + ' ' + sentiment['docSentiment']['score'] + ' '
    for word in keywords['keywords']:
        tweet['keywords'] = tweet['keywords'] + word['text'] + ' ' + word['relevance'] + ' '
    tweetChunks.append(tweet)

# Analyse all text together
overallResult = {}
overallResult['chunk'] = allText
keywords = alchemy.keywords('text', allText)
overallResult['keywords'] = ''
# Call AlchemyAPI to get keywords and sentiment for all text together
sentimentType = alchemy.sentiment('text',allText)['docSentiment']['type']
sentimentScore = alchemy.sentiment('text',allText)['docSentiment']['score']
overallResult['sentiment'] = sentimentType + ' ' + sentimentScore + ' '
for word in keywords['keywords']:
    overallResult['keywords'] = overallResult['keywords'] + word['text'] + ' ' + word['relevance'] + ' '

# Write processed chunks to 'tweetChunks2.txt'
fout = open('tweetChunks2.txt', 'wb')
writer = csv.writer(fout, delimiter='\t')
for item in range(0, len(tweetChunks)):
	writer.writerow([tweetChunks[item]['chunk'], tweetChunks[item]['keywords'], tweetChunks[item]['sentiment']])
writer.writerow([overallResult['chunk'], overallResult['keywords'], overallResult['sentiment']])
fout.close()
