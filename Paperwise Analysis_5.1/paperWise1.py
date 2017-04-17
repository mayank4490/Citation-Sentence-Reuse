#!/home/mayank/anaconda/bin/python
import os
import sys
import sklearn
import matplotlib
import pickle

matplotlib.use('Agg')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity

"""
Input:  Is a file that contains
        '<cited> <citer> <citation context>' information.
        Update that filename in the variable dataFile

Output: Produces tuples
        '<citer1> <citer2> <cited> <cosineSimilarity>'
         stored in outputDataFrame
"""

def get_years():
    year_of = {}
    with open("../Files/years_final.txt", "r") as years_file:
        for line in years_file.readlines():
            line = line.split(":")            
            year_of[int(line[0])] = int(line[1])
    return year_of


def get_titles():
    title_of = {}
    with open("../Files/paper_title", "r") as titles_file:
        for line in titles_file.readlines():
            line = line.split()
            context = ' '.join(line[1:])            
            title_of[int(line[0])] = context
    return title_of

def paper_fields():
    field_of = {}
    with open("../Files/paper_fields", "r") as fields_file:
        for line in fields_file.readlines():
            line = line.split()            
            field_of[int(line[0])] = str(line[1])
    return field_of



# print sys.executable
# print pd.__version__


dataFile = "../Files/cited_citer_dump_processed_v3"




sampleStopWords = ['CITATION','I','a','an','are','as','at','be','by','for','from','in','is','it','of','on','or','that','the','this','to','was','will','with']
citer = []
cited = []
citationContext = []


inputFile = open(dataFile, 'r')
allLines = inputFile.readlines()

print "Input File has been read"

lineNum = 0
for line in allLines:
    lineNum += 1
    if lineNum < 24:
      continue
    line = line.split(' ')
    cited.append(int(line[0]))
    citer.append(int(line[1]))
    citationContext.append(' '.join(line[2:]))
#print len(citer)

inputData = list(zip(citer, cited, citationContext))
inputDataFrame = pd.DataFrame(data = inputData, columns = ['Citer', 'Cited', 'Citation Context'])

print "inputDataFrame is created"

inputDataFrame = inputDataFrame.sort_values(['Cited'], ascending = [True])
inputDataFrame = pd.DataFrame(data = inputDataFrame ,columns = ['Citer', 'Cited', 'Citation Context'])

#print inputDataFrame
inputDataFrame = inputDataFrame.reset_index(drop=True)
#print inputDataFrame

print "inputDataFrame has been sorted according to the *Cited* column"

# print len(inputDataFrame['Citer'].unique())
inputDataFrame['ccLength'] = inputDataFrame['Citation Context'].apply(lambda x: len(x))
print inputDataFrame['ccLength'].mean() 
exit()

groupedData = inputDataFrame.groupby('Cited').size().to_frame(name='Citers Count').reset_index().sort_values('Citers Count', ascending=False).reset_index(drop=True)
#print groupedData
top500Papers = groupedData['Cited'].head(n=500)
#print top500Papers

top500PapersCitationData = inputDataFrame[inputDataFrame['Cited'].isin(top500Papers)]
top500PapersCitationData = top500PapersCitationData.reset_index(drop=True)
#print top500PapersCitationData

paperYearDataDict = get_years()
paperFields = paper_fields()


rows = top500PapersCitationData.shape[0]
top500PapersCitationData['Cited-Year'] = [0]*rows
top500PapersCitationData['Citer-Year'] = [0]*rows
top500PapersCitationData['Year Difference'] = [0]*rows
top500PapersCitationData['Cosine-Similarity'] = [0]*rows
#print "Length of top500PapersCitationData: ", rows



for index, row in top500PapersCitationData.iterrows():
    # print "Current Iteration in top500PapersCitationData.iterrows(): ", index, "in total of: ", rows    
    if(index % 1000 == 0):
  print "Current: ", index, "in total: ", rows
    try:
        citedPaper = int(row['Cited'])
        citedYear = paperYearDataDict[citedPaper]
    except:
        citedYear = -1
    try:
        citerPaper = int(row['Citer'])
        citerYear = paperYearDataDict[citerPaper]
    except:
        citerYear = -1
    #print "CitedYear", citedYear
    #print "CiterYear", citerYear

    top500PapersCitationData.iat[index, 3] = citedYear
    top500PapersCitationData.iat[index, 4] = citerYear    
    top500PapersCitationData.iat[index, 5] = citerYear - citedYear if (citerYear-citedYear>=0 and citerYear != -1) else -1

#print top500PapersCitationData

top500PapersCitationData = top500PapersCitationData[top500PapersCitationData['Year Difference'].isin([0,1,2,3,4,5])]
top500PapersCitationData = top500PapersCitationData.reset_index(drop=True)
#print "Print Top500PapersData: ", top500PapersCitationData

top500PapersCitationData.to_pickle('top500PapersData.p')
# top500PapersCitationData = pd.read_pickle('top500PapersData.p')

citationContext = list(top500PapersCitationData['Citation Context'])
# print citationContext
citationContext = [string[:-1] for string in citationContext]
# print 'Citation Contexts', citationContext

myStopWords = text.ENGLISH_STOP_WORDS.union('CITATION','citation')

vectorizer = TfidfVectorizer(analyzer='word' , stop_words= set(myStopWords), lowercase=True, max_features=100000)
tfidf = vectorizer.fit_transform(citationContext)

# #tfidf = pickle.load( open( "tfidftop10.p", "rb" ) )
# pickle.dump(tfidf, open('tfidf.p', 'wb'))

# # print tfidf
# print 'Size of tf-idf Vector: ', tfidf.shape
# print "tfidf Vector Generated"


year = [0]*6

for i in xrange(1,6):
    year[i] = pd.DataFrame(columns = ['Cited', 'Citer1', 'Citer2', 'Citation Context', 'CosineSimilarity', 'Category', 'Category2', 'Context-Title Similarity'])

paperAuthorDict = {}

with open("../Files/paper_author_sorted", 'r') as f:
    for line in f:
        items = line.split()
        key, values = int(items[0]), items[1:]
        paperAuthorDict[key] = values

# print paperAuthorDict

paperTitleDataDict = get_titles()
# print paperTitleDataDict

groupedData = top500PapersCitationData.groupby('Cited')
for name, group in groupedData:
    print "Calculating for: ", name
    indexes = list(groupedData.groups[name])
    print "Indexes: ", indexes
    # print indexes, len(indexes)

    for ithIndex, i in enumerate(indexes):
        for j in indexes[ithIndex+1:]:
            # print "Indexes: ", indexes
            # print "indexes[ithIndex]: ", indexes[ithIndex]
            # print "j: ", j
            # print "Iteration No: ", j, " in total: ", len(indexes)
            cited = []
            citer1 = []
            citer2 = []
            context = []
            cited.append(top500PapersCitationData.iat[i, 1])
            citer1.append(top500PapersCitationData.iat[i, 0])
            citer2.append(top500PapersCitationData.iat[j, 0])
            citer1Year = (int(top500PapersCitationData.iat[i, 5]))
            citer2Year = (int(top500PapersCitationData.iat[j, 5]))
            # print "Process Executing for: Cited -> ", int(cited) , " Citer1 -> ", int(citer1), " Citer2 -> ", int(citer2)
            
            indexTakenContextTitleSim = i
            # print "Cited:", cited
            # print "Citer1:", citer1
            # print "Citer2:", citer2
            # print "Citer1Year:", citer1Year
            # print "Citer2Year:", citer2Year



            if(citer1Year == citer2Year):
                continue

            if(citer2Year > citer1Year):
                [citer1, citer2] = [citer2, citer1]
                [citer1Year, citer2Year] = [citer2Year, citer1Year]
                indexTakenContextTitleSim = j

            dataCorrespondstoYear = citer1Year
            # print dataCorrespondstoYear
            context.append(top500PapersCitationData.iat[i,2])

            cosineSimilarity = cosine_similarity(tfidf[i], tfidf[j])
            # print top500PapersCitationData.iloc[i, 2]
            # print top500PapersCitationData.iloc[j, 2]
            # print int(cited), int(citer1), int(citer2), float(cosineSimilarity)
            category = [0]*1
            category2 = [0]*1
            category[0] = 'NN'
            category2[0] = 'NN'
            if(cosineSimilarity < 0.8):
                continue

            if(cosineSimilarity >= 0.8):
                try:
                    paper1Auth = set(paperAuthorDict[int(citer1[0])])
                    paper2AUth = set(paperAuthorDict[int(citer2[0])])
                    authFound = 1
                except:
                    authFound = 0

                
                if(authFound == 1):
                    if (paper1Auth & paper2AUth):
                        category[0] = 'SC'
                    else:
                        if((any(inputDataFrame.Citer == int(citer1[0]) and (inputDataFrame.Cited == int(citer2[0]))))  or (any(inputDataFrame.Citer == int(citer2[0]) and (inputDataFrame.Cited == int(citer1[0]))))):
                            category[0] = 'CC'
                        else:
                            category[0] = 'CN'
                else:
                    if((any(inputDataFrame.Citer == int(citer1[0]) and (inputDataFrame.Cited == int(citer2[0]))))  or (any(inputDataFrame.Citer == int(citer2[0]) and (inputDataFrame.Cited == int(citer1[0]))))):
                        category[0] = 'CC'
                    else:
                        category[0] = 'CN'

            if(cosineSimilarity >= 0.8):
                if((any(inputDataFrame.Citer == int(citer1[0]) and (inputDataFrame.Cited == int(citer2[0]))))  or (any(inputDataFrame.Citer == int(citer2[0]) and (inputDataFrame.Cited == int(citer1[0]))))):
                    category2[0] = 'CC'
                else:
                    category2[0] = 'CN'

            print "Citer1: ", int(citer1)
            contextTitleSimilarity = [0]*1
            try:
                citer1Title = paperTitleDataDict[int(citer1[0])]
            except:
                citerTitle = 0
                # Do Nothing
            if(citer1Title):
                # print "Citer1 Title Found: ", citer1Title
                titleTfIdf = vectorizer.transform([citer1Title])
                # print "TitelTfIdf: ", titleTfIdf, titleTfIdf.shape
                contextTitleSimilarity = cosine_similarity(tfidf[indexTakenContextTitleSim], titleTfIdf)
            else:
                # print "Title not found for Paper %d"  %(int(citer1))
                contextTitleSimilarity = [0]*1

            tempData = list(zip(cited, citer1, citer2, context, cosineSimilarity, category, category2, contextTitleSimilarity))
            # print int(cited), int(citer1), int(citer2), float(cosineSimilarity), category, category2, contextTitleSimilarity

            tempDataFrame = pd.DataFrame(data = tempData, columns = ['Cited', 'Citer1', 'Citer2', 'Citation Context','CosineSimilarity', 'Category', 'Category2', 'Context-Title Similarity'])
            # print tempDataFrame.iloc[0,4]
            
            year[dataCorrespondstoYear] = year[dataCorrespondstoYear].append(tempDataFrame, ignore_index=True)
            fname = 'year%dtop10.p' %(dataCorrespondstoYear)
            year[dataCorrespondstoYear].to_pickle(fname)          
# print year[1]['Context-Title Similarity']            




for i in xrange(1,6):
    year[i]['CosineSimilarity'] = year[i]['CosineSimilarity'].str[0]
    year[i]['Citer1'] = year[i]['Citer1'].astype(int)
    year[i]['Citer2'] = year[i]['Citer2'].astype(int)
    year[i]['Cited'] = year[i]['Cited'].astype(int)
    year[i]['Context-Title Similarity'] = year[i]['Context-Title Similarity'].str[0]
    year[i]['Category'] = year[i]['Category'].astype(str)
    year[i]['Category2'] = year[i]['Category2'].astype(str)
    year[i]['Citation Context'] = year[i]['Citation Context'].astype(str)
    year[i]['Paper Field'] = year[i]['Cited'].apply(lambda x: paperFields[x] if (x in paperFields) else 'NA')
    fname = 'year%dtop10.p' %(i)
    year[i].to_pickle(fname)


# for i in xrange(1,6):
#     fname = 'year%dtop10.p' %(i)
#     year[i] = pd.read_pickle(fname)


for i in xrange(1,6):
    for index, row in year[i].iterrows():
        citer1 = citer2 = [0]*1
        citer1[0] = row['Citer1']
        citer2[0] = row['Citer2']
        # print row['Category'], row['Category2']
        if(row['Category'] == 'CC' or row['Category'] == 'CN'):
            # print "idhar aaya"
            if(((inputDataFrame.loc(inputDataFrame['Citer']==int(citer1[0]))).apply(int) & (inputDataFrame.loc(inputDataFrame['Cited']==int(citer2[0]))).apply(int)) | ((inputDataFrame.loc(inputDataFrame['Citer']==int(citer2[0]))).apply(int) & (inputDataFrame.loc(inputDataFrame['Cited']==int(citer1[0]))).apply(int))):
                category[0] = 'CC'
            else:
                category[0] = 'CN'
        
        if(((inputDataFrame.loc(inputDataFrame['Citer']==int(citer1[0]))).apply(int) & (inputDataFrame.loc(inputDataFrame['Cited']==int(citer2[0]))).apply(int)) | ((inputDataFrame.loc(inputDataFrame['Citer']==int(citer2[0]))).apply(int) & (inputDataFrame.loc(inputDataFrame['Cited']==int(citer1[0]))).apply(int))):
            category2[0] = 'CC'
        else:
            category2[0] = 'CN'

    year[i]['Category'] = year[i]['Category'].astype(str)
    year[i]['Category2'] = year[i]['Category2'].astype(str)






countsAnnualCategory = [0]*5
totalAnnualCitaions = [0]*5

for i in xrange(0,5):
    totalAnnualCitaions[i] = len(year[i+1].Category)
    countsAnnualCategory[i] = year[i+1].groupby('Category').size().to_frame(name='Category Count').reset_index().sort_values('Category', ascending=False).reset_index(drop=True)

SC = [0]*5
CC = [0]*5
CN = [0]*5

for i in xrange(0,5):
    try:
        row = countsAnnualCategory[i].loc[countsAnnualCategory[i]['Category'] == "SC"]
        SC[i] = row.iloc[0, 1]
        SC[i] = float(SC[i])/float(totalAnnualCitaions[i])
    except:
        SC[i] = 0
    # print SC[i]

    try:
        row = countsAnnualCategory[i].loc[countsAnnualCategory[i]['Category'] == "CC"]
        CC[i] = row.iloc[0, 1]
        CC[i] = float(CC[i])/float(totalAnnualCitaions[i])
    except:
        CC[i] = 0
    # print CC[i]

    try:
        row = countsAnnualCategory[i].loc[countsAnnualCategory[i]['Category'] == "CN"]
        CN[i] = row.iloc[0, 1]
        CN[i] = float(CN[i])/float(totalAnnualCitaions[i])
    except:
        CN[i] = 0
    # print CN[i]


fname = "paperWise1SC" 
with open(fname, "w") as citation_file:
    pickle.dump(SC, citation_file)

fname = "paperWise1CC" 
with open(fname, "w") as citation_file:
    pickle.dump(CC, citation_file)

fname = "paperWise1CN" 
with open(fname, "w") as citation_file:
    pickle.dump(CN, citation_file)




countsAnnualCategory = [0]*5
totalAnnualCitaions = [0]*5

for i in xrange(0,5):
    totalAnnualCitaions[i] = len(year[i+1].Category2)
    countsAnnualCategory[i] = year[i+1].groupby('Category2').size().to_frame(name='Category2 Count').reset_index().sort_values('Category2', ascending=False).reset_index(drop=True)

CC = [0]*5
CN = [0]*5

for i in xrange(0,5):
    try:
        row = countsAnnualCategory[i].loc[countsAnnualCategory[i]['Category2'] == "CC"]
        CC[i] = row.iloc[0, 1]
        CC[i] = float(CC[i])/float(totalAnnualCitaions[i])
    except:
        CC[i] = 0
    # print CC[i]

    try:
        row = countsAnnualCategory[i].loc[countsAnnualCategory[i]['Category2'] == "CN"]
        CN[i] = row.iloc[0, 1]
        CN[i] = float(CN[i])/float(totalAnnualCitaions[i])
    except:
        CN[i] = 0
    # print CN[i]


fname = "paperWise2CC" 
with open(fname, "w") as citation_file:
    pickle.dump(CC, citation_file)

fname = "paperWise2CN" 
with open(fname, "w") as citation_file:
    pickle.dump(CN, citation_file)

# year[i].to_csv('temp.csv', index=False)

