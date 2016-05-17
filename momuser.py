import twitter
import oauthDance
import json
import csv
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

t = oauthDance.login()

moms = t.users.search(q="mother")
moms += t.users.search(q="mom")
moms += t.users.search(q="mama")
moms += t.users.search(q="mommy")
moms += t.users.search(q="mom-to-be")

goodMoms = []

for mom in moms:
	if mom['description'].find('mother')!=-1 or mom['description'].find('mom')!=-1 or mom['description'].find('mama')!=-1 or mom['description'].find('mommy')!=-1 or mom['description'].find('mom-to-be')==True:
		momDict = {}
		momDict['screen_name'] = mom['screen_name']
		momDict['desc'] = mom['description']
		goodMoms.append(momDict)


fout = open('moms.txt', 'wb')
writer = csv.writer(fout, delimiter='\t')
writer.writerow(['screen_name', 'description'])
for item in range(0, len(goodMoms)):
	writer.writerow([goodMoms[item]['screen_name'], goodMoms[item]['desc']])

fout.close()
