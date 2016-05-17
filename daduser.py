import twitter
import oauthDance
import json
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

t = oauthDance.login()

dads = t.users.search(q="father")
dads += t.users.search(q="dad")
dads += t.users.search(q="dada")
dads += t.users.search(q="daddy")
dads += t.users.search(q="dad-to-be")

goodDads = []

for dad in dads:
	if dad['description'].find('father')!=-1 or dad['description'].find('dad')!=-1 or dad['description'].find('dada')!=-1 or dad['description'].find('daddy')!=-1 or dad['description'].find('dad-to-be')==True:
		dadDict = {}
		dadDict['screen_name'] = dad['screen_name']
		dadDict['desc'] = dad['description']
		goodDads.append(dadDict)


fout = open('dads.txt', 'wb')
writer = csv.writer(fout, delimiter='\t')
writer.writerow(['screen_name', 'description'])
for item in range(0, len(goodDads)):
	writer.writerow([goodDads[item]['screen_name'], goodDads[item]['desc']])

fout.close()
