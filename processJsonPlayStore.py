from enum import unique
import json
from numpy import NaN
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import sys
from scipy import spatial
bagOfWords=[]
allComments=[]
wordFrequency={}

headlines = [
#Crypto
'Investors unfazed by correction as crypto funds see $154 million inflows',
'Bitcoin, Ethereum prices continue descent, but crypto funds see inflows',
 
#Inflation
'The surge in euro area inflation during the pandemic: transitory but with upside risks',
"Inflation: why it's temporary and raising interest rates will do more harm than good",
 
#common
'Will Cryptocurrency Protect Against Inflation?']

"""
def vectorize(tokens):
    ''' This function takes list of words in a sentence as input 
    and returns a vector of size of filtered_vocab.It puts 0 if the 
    word is not present in tokens and count of token if present.'''
    vector=[]
    for w in final_words:
        vector.append(tokens.count(w))
    return vector
"""

def create_heatmap(similarity):
  df = pd.DataFrame(similarity)
  df.columns = headlines
  df.index = headlines
  fig, ax = plt.subplots(figsize=(5,5))
  sns.heatmap(df)
  plt.show()

# Opening JSON file
f = open('reviewsGooglePlay.json')
 
# returns JSON object as
# a dictionary
data = json.load(f)

for element in data:
    applicationName = element
    for object in data[element]:
        review = object["review"]
        if (review is NaN):
            review = review.strip('\n')
        review = review.lower()
        allComments.append(review)

labels = [headline[:20] for headline in headlines]

dataSetI = ['hello', 'my', 'name', 'is', 'alberto']
dataSetII = ['i', 'am', 'called', 'alberto']
result = 1 - spatial.distance.cosine(dataSetI, dataSetII)
print(result)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(labels)
arr = X.toarray()
print(arr)
#create_heatmap(cosine_similarity(arr))




 
"""
#split the sentences into tokens
i=1
dictionary={}
for comment in allComments:
    dictionary["token" + str(i)] = comment.split()
    i+=1

vocabulary=[]
for key, value in dictionary.items():
    for elm in value:
        vocabulary.append(elm)

final_words = list(set(vocabulary))


#convert sentences into vectords
first_value=list(dictionary.values())[0]
vector1=vectorize(first_value)
print(vector1)

"""

# Closing file
f.close()

