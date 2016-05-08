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
dictionary={}
#open dictionary from file

file=open("keyword_dictionary_fixed_1.CSV", "r")
	reader = csv.reader(file)
	for row_ls in reader:
		a=Keyword(row_ls[1],row_ls[2],row_ls[3],row_ls[4])
		dictionary[row_ls[0]]=a
	keys_list=dictionary.keys()
	with open('keyword_dictionary_fixed_c.csv', 'w') as fp:
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
