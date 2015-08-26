#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

endpoint = 'https://mattermark.com/category/mattermark-daily/page/'
stop = stopwords.words('english')

class Daily:
	def __init__(self, art):
		s = art.find('h1', {'class': 'entry-title'}).a
		self.url = s.attrs['href']
		self.title = s.text
		self.content = clean_string(art.text)
		
		try:
			self.date = self.title.encode('utf-8').split(' – ')[1]
		except:
			self.date = 'missing'

def clean_string(string):
	pattern = re.compile('[\W_]+', re.UNICODE)
	return pattern.sub(' ', string)

def main():
	dailies = []

	i = 1
	while True:
		r = requests.get(endpoint + str(i))
		if r.status_code != 200:
			break
		html = r.content
		soup  = BeautifulSoup(html)
		articles = soup.find_all('article')
		for art in articles:
			dailies.append(Daily(art))
		print i
		i+=1
	dailies.reverse()
	docs = [d.content for d in dailies]
	dates = [d.date.replace(',','') for d in dailies]
	vectorizer = CountVectorizer( analyzer = 'word', \
								  decode_error = 'replace', \
								  min_df=15, \
								  ngram_range=(1,3),\
								  stop_words = stop)
	data = vectorizer.fit_transform(docs).toarray()
	vocab = vectorizer.get_feature_names()
	
	df = pd.DataFrame(data, index=dates, columns=vocab)

	sums = list(df.sum(axis=0))

	df.to_csv('mattermark.csv', index=True, header=True, sep=',')

	counts = sorted(zip(vocab,sums),key=lambda x: x[1])

	print data.shape
	print len(vocab)
	for pair in counts[-100:]:
		print pair[0], pair[1]

if __name__ == '__main__':
	main()