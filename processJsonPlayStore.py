from enum import unique
import json
from numpy import NaN
from sklearn.feature_extraction.text import CountVectorizer

bagOfWords=[]
allComments=[]
wordFrequency={}


def vectorize(tokens):
    ''' This function takes list of words in a sentence as input 
    and returns a vector of size of filtered_vocab.It puts 0 if the 
    word is not present in tokens and count of token if present.'''
    vector=[]
    for w in final_words:
        vector.append(tokens.count(w))
    return vector

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

# Closing file
f.close()

