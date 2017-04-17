#!/home/mayank/anaconda/bin/python
import os
import sys
import sklearn
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import cPickle as pickle
from collections import defaultdict
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_years():
	year_of = {}
	with open("../Files/years_final.txt", "r") as years_file:
		for line in years_file.readlines():
			line = line.split(":")			
			year_of[int(line[0])] = int(line[1])
	return year_of

def get_authors():
	'''Returns a dict (indexed by paperid) of sets of authors'''
	authors_of = {}
	with open("../Files/paper_author_sorted", 'r') as f:
		for line in f:
			items = line.split()
			paper, authors = int(items[0]), [int(author) for author in items[1:]]
			authors_of[paper] = set(authors)
	return authors_of

def get_titles():
	title_of = {}
	with open("../Files/paper_title", "r") as titles_file:
		for line in titles_file.readlines():
			line = line.split()
			context = ' '.join(line[1:])			
			title_of[int(line[0])] = context
	return title_of

def get_fields():
	field_of = {}
	with open("../Files/paper_fields", "r") as fields_file:
		for line in fields_file.readlines():
			line = line.split()			
			field_of[int(line[0])] = line[1]
	return field_of

year_of = get_years()
authors_of = get_authors()
title_of = get_titles()
field_of = get_fields()
print "Metadata loaded"

citers = []
citeds = []
# fields = []
citationContexts = []

lineNum = 0
with open("../Files/cited_citer_dump_processed_v3", 'r') as inputFile:
	for line in inputFile:
		lineNum += 1
		if lineNum < 24:
			continue	
		line = line.split(' ')
		if int(line[1]) not in year_of:
			continue
		if int(line[1]) not in authors_of:
			continue
		if int(line[0]) not in authors_of:
			continue
		if int(line[1]) not in title_of:
			continue
		if int(line[0]) not in field_of:
			continue
		citeds.append(int(line[0]))
		citers.append(int(line[1]))
		# fields.append(str(field_of[int(line[0])]))
		citationContexts.append(' '.join(line[2:]))

		# if lineNum == 1000:
		# 	break
print "cited_citer_dump_processed_v3 has been read"

inputData = zip(citers, citeds, citationContexts)
inputDataFrame = pd.DataFrame(data = inputData, columns = ['Citer', 'Cited', 'Citation Context'])
print "Size of inputData: ", len(inputData)

# citationContexts = list(inputDataFrame['Citation Context'])
citationContexts = [string[:-1] for string in citationContexts]
# print citationContext
myStopWords = text.ENGLISH_STOP_WORDS.union('CITATION','citation')
# Note: tolower is default behaviour for TfidfVectorizer
vectorizer = TfidfVectorizer(analyzer='word' , stop_words=set(myStopWords), max_features=100000, lowercase=True)
tfidf = vectorizer.fit_transform(citationContexts)
 # print tfidf
print 'tf-idf Vectors generated. Size: ', tfidf.shape
with open("tfidfvectorizer", "w") as vector_file:
	pickle.dump(vectorizer, vector_file)
print "Vectorizer saved to file"

#vectorizer = pickle.load(open("pickle/tfidfvectorizer", "r"))
#tfidf = vectorizer.transform(citationContexts)
#print 'tf-idf Vectors loaded from file. Size: ', tfidf.shape


# citationDataFrame = pd.DataFrame(columns = ["cited", "citer", "maxCosine", "category"])
citationData = []
# pairwiseDataFrame = pd.DataFrame(columns = ["cited", "copier", "copyfrom", "cosine", "category"])
pairwiseData = []

totalCitationsCount = 0
copiedCount = 0
selfCopiedCount = 0
selfTitleCopiedCount = 0
multipleCopiedCount = 0
selfCopyingAuthors = set()
copyingAuthors = set()
cosine_values = defaultdict(list)

groupedCiteds = defaultdict(list)
groupedFields = defaultdict(list)

for index, cited in enumerate(citeds):
	groupedCiteds[cited].append(index)
print "Created cited groups"

# for index, field in enumerate(fields):
# 	groupedFields[field].append(index)
# print "Created field groups"

totalNumberOfCitation = 0
fieldWiseCitation = {}

print "Finding cosine similarities..."
groupNo = 0
for cited in groupedCiteds.keys():
	groupNo += 1
	indexes = groupedCiteds[cited]
	totalNumberOfCitation += len(indexes)
	try:
		fieldWiseCitation[field_of[int(cited)]] += len(indexes)
	except:
		fieldWiseCitation[field_of[int(cited)]] = len(indexes)
	# print "Indexes: ", Indexes
	# print indexes, len(indexes)
	print "Calculating for groupNo: ", groupNo, "/", len(groupedCiteds), " len: ", len(indexes)
	print cited


	for i in indexes:
		citerCopied = False
		selfCopied = False
		selfTitleCopied = False
		maxCosine = 0

		totalCitationsCount += 1

		citeri = citers[i]
		citeriYear = year_of[citeri]

		for j in indexes:
			if i == j:
				continue

			citerj = citers[j]
			citerjYear = year_of[citerj]

			# citeri cannot be copied from citerj
			if citeriYear <= citerjYear:
				continue		
			category = [0]*1
			category2 = [0]*1
			pairCategory = "NC"
			cosine = cosine_similarity(X = tfidf[i], Y = tfidf[j])
			if cosine > maxCosine:
				maxCosine = cosine[0, 0]

			if(cosine[0,0] >= 0.8):
				paper1Auth = set(authors_of[citeri])
				paper2AUth = set(authors_of[citerj])
				if (paper1Auth & paper2AUth):
						category[0] = 'SC'
				else:
					if((any(inputDataFrame.Citer == citeri and inputDataFrame.Cited == citerj))  or (any(inputDataFrame.Citer == citerj and inputDataFrame.Cited == citeri))):
						category[0] = 'CC'
					else:
						category[0] = 'CN'

			if(cosine[0,0] >= 0.8):
				if((any(inputDataFrame.Citer == citeri and inputDataFrame.Cited == citerj))  or (any(inputDataFrame.Citer == citerj and inputDataFrame.Cited == citeri))):
						category2[0] = 'CC'
					else:
						category2[0] = 'CN'

			if(cosine[0,0] < 0.8):
				category[0] = ''
				category2[0] = ''

			listElement = (cosine[0, 0], category[0], category2[0])
			cosine_values[field_of[int(cited)]].append(listElement)

			

	if groupNo % 5000 == 0: # Generate outputs
		fname = "fields%d" %(groupNo/100)
		with open(fname, "w") as citation_file:
			pickle.dump(cosine_values, citation_file)
		fname = "fields%dCCcount" %(groupNo/100)
		with open(fname,"w") as countFile:
			pickle.dump(totalNumberOfCitation, countFile)
		fname = "fields%dFieldcount" %(groupNo/100)
		print fieldWiseCitation
		with open(fname,"w") as fieldFile:
			pickle.dump(fieldWiseCitation, fieldFile)


