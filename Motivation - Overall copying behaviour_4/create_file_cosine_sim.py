import string
#import pandas
import re
import sklearn

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

citedciter = open('../cited_citer_dump_processed_v3')
#cosineValues = open('cosineSimilarityValues.csv')
context = dict()
t = tuple()
count = 0
for line in citedciter:
	line = line.rstrip()
	# print "line ->", line
	# print "end"
	t = ( str(re.findall('(^[0-9]+) [0-9]+ \S+', line))[2:-2], str(re.findall('^[0-9]+ ([0-9]+) \S+',line ))[2:-2]) 
	#print t

	if t != ("",""):
		# if valid line in dump file
		if context.get(t, 0) is 0 :
			count=count+1
			context[t] = re.findall('[0-9]+ [0-9]+ (.+)$', line)
		else:
			context[t][0] += (" " + str(re.findall('[0-9]+ [0-9]+ (.+)$', line))[2:-2]) #append space separated context

citation_for_tfidf = list() 

InOrder = sorted(context)  #list of (cited citer) tuples in sorted order
print "Length of in order ",len(InOrder) # number of unique citer cited pairs 

item = tuple()
for item in InOrder:
	citation_for_tfidf += context[item]        #list of contexts for tifidf training


sampleStopWords = ['CITATION','I','a','an','are','as','at','be','by','for','from','in','is','it','of','on','or','that','the','this','to','was','will','with']
tfidf = TfidfVectorizer(analyzer='word' , stop_words=sampleStopWords).fit_transform(citation_for_tfidf)
#tfidf vector of contexts in same order as inorder

for item, vectemp in zip(InOrder, tfidf):
	context[item].append(vectemp) # now context 

#access the tfidf for any citation context like this : context[item][1]    here item is the tuple of citer cited  
linkExists = dict()
noLinkExists = dict()
le=0
nle=0

fdumpofcosine = open('../cited_citer1_citer2_concatenated_cosine_similarity','w')


for idx, item in enumerate(InOrder):

	idx = (idx +1)%len(InOrder) -1
	if (InOrder[idx+1][0] == item[0]) and (context.get((InOrder[idx+1][1],item[1]), None) is not None or context.get((item[1], InOrder[idx+1][1]), None) is not None) :    #cited paper same
		#cited same and link exists that means the two citers have cited each other (depending on whose paper was
		# published later)
		#print "1"
		fdumpofcosine.write(re.findall('[0-9]+',str(item))[0])
		fdumpofcosine.write(" ")
		fdumpofcosine.write(re.findall('[0-9]+',str(item))[1])
		fdumpofcosine.write(" ")
		fdumpofcosine.write(InOrder[idx+1][1])
		fdumpofcosine.write(" ")
		fdumpofcosine.write(str(cosine_similarity(context[item][1],context[InOrder[idx+1]][1]))[3:-2])
		fdumpofcosine.write(" ")
		if(context.get((InOrder[idx+1][1],item[1]), None) is not None):
			fdumpofcosine.write("Link Exists: citerOne has cited citerTwo")
		else:
			fdumpofcosine.write("Link Exists: citerTwo has cited citerOne")
		fdumpofcosine.write("\n")
		if len(linkExists) >100000:
			continue
		linkExists[(InOrder[idx+1][1],item[1])] = cosine_similarity(context[item][1],context[InOrder[idx+1]][1])
	elif (InOrder[idx+1][0] == item[0]) and not (context.get((InOrder[idx+1][1],item[1]), None) is not None or context.get((item[1], InOrder[idx+1][1]), None) is not None) :    #cited paper same
		#cited same and link does not exist
		#print "2"
		fdumpofcosine.write(re.findall('[0-9]+',str(item))[0])
		fdumpofcosine.write(" ")
		fdumpofcosine.write(re.findall('[0-9]+',str(item))[1])
		fdumpofcosine.write(" ")
		fdumpofcosine.write(InOrder[idx+1][1])
		fdumpofcosine.write(" ")
		fdumpofcosine.write(str(cosine_similarity(context[item][1],context[InOrder[idx+1]][1]))[3:-2])
		fdumpofcosine.write(" ")
		fdumpofcosine.write("No link exists")
		fdumpofcosine.write("\n")                

#print len(linkExists), len(noLinkExists)
