
import csv
import urllib
from lxml.html import fromstring


class Keyword(object):

    def __init__(self, a0, a1, a2,a3):
        self.min = a0
        self.max = a1
        self.tot = a2
        self.num = a3

es=0
#open dictionary from file

	#file=open("keyword_dictionary_4.CSV", "r")
	#reader = csv.reader(file)

	#for row_ls in reader:
	#	a=Keyword(row_ls[1],row_ls[2],row_ls[3],row_ls[4])
#		dictionary[row_ls[0]]=a
	#for line in fp:
	
dictionary={}

links=open('urls_0.txt','r')
links=links.readlines()
for link in links:
	url=link
	content = urllib.urlopen(url).read()
	doc = fromstring(content)
	doc.make_links_absolute(url)

	kw=doc.xpath('.//meta[@name="keywords"]/@content')
			#print('keywords ') + str(kw)
	kw_ls=kw[0].split(', ')
			#print('number of keywords: ') + str(len(kw[0].split()))
			#print('number of total shares :')

	sh=doc.find_class("total-shares")
	shares_str=sh[0].text_content().split()[0]

	if(shares_str.find('k')!=-1):
		s=shares_str.split('k')[0]
		shares=float(s)*1000
		shares=int(shares)
	else:
		if(shares_str.find('M')!=-1):
			s=shares_str.split('M')[0]
			shares=float(s)*1000000
			shares=int(shares)
		else:
			if(shares_str.find(',')!=-1):
				s=shares_str.split(',')[0]
				s0=shares_str.split(',')[1]
				n=s+s0
				shares=int(n)
			else:
				shares=int(shares_str)
			#print shares 

	default=0
	for i in kw_ls:
		v=dictionary.get(i, default)

		if(v!=default):
			if (shares<v.min):
				v.min=shares
			if(shares>v.max):
				v.max=shares
			v.num=int(v.num)+1
			v.tot=int(v.tot)+int(shares)
		else:			
			if(v==default):
				a=Keyword(shares,shares,shares,1)
				dictionary[i]=a
	es=es+1
	print es


keys_list=dictionary.keys()
with open('keyword_dictionary_fixed_1.csv', 'w') as fp:
	r = csv.writer(fp, delimiter=',')
			#data=[['kw', 'min', 'max', 'tot', 'num']]
			#r.writerows(data)
	for i in keys_list:
		data=[[i,
			dictionary[i].min,
			dictionary[i].max,
			dictionary[i].tot,
			dictionary[i].num]]
		r.writerows(data)
		







