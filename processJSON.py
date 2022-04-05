#word mover distance
import logging

from numpy import vectorize
from torch import combinations
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from nltk.corpus import stopwords
from nltk import download
import gensim.downloader as api

#bag of words cosine similarity
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))

#bert cosine similarity
import pandas as pd
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

#bag of words universal sentence encoder
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

#obtain comments
import json
import itertools


def preprocess_word_mover_distance(sentence, stop_words):
    return [w for w in sentence.lower().split() if w not in stop_words]

#Word embedings (bag of words) + word mover distance
def word_mover_distance(lista):

    download('stopwords')  # Download stopwords list.
    stop_words = stopwords.words('english')

    for comment1, comment2 in itertools.combinations(lista, 2):

        #sentence_obama = 'Obama speaks to the media in Illinois'
        #sentence_president = 'The president greets the press in Chicago'

        first_sentence = preprocess_word_mover_distance(comment1, stop_words)
        second_sentence = preprocess_word_mover_distance(comment2, stop_words)

        model = api.load('word2vec-google-news-300')
        distance = model.wmdistance(first_sentence, second_sentence)
        print('The distance between', first_sentence, " and ", second_sentence, 'is', distance)

def preporcess_cosine_similarity(text):
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text =' '.join([word for word in text.split() if word not in stop_words])
    return text

def cosine_sim_vectors(vector1, vector2):
    vector1 = vector1.reshape(1, -1)
    vector2 = vector2.reshape(1, -1)
    return cosine_similarity(vector1, vector2)[0]

def bag_of_words_consine_similarity():
    sentences = ["I ate dinner.", 
       "We had a three-course meal us.", 
       "Brad came to dinner with us.",
       "He loves fish tacos.",
       "In the end, we all felt like we ate too much.",
       "We all agreed; it was a magnificent evening."]
    cleaned = list(map(preporcess_cosine_similarity, sentences))
    #print(results)
    vectorizer = CountVectorizer().fit_transform(cleaned)
    vectors = vectorizer.toarray()
    #print(vectors)
    csim = cosine_sim_vectors(vectors[0], vectors[1])
    print("Similarity between sentence (", sentences[0], ") and sentence (", sentences[1], ") is:", csim)

def most_similar(doc_id,similarity_matrix,matrix,documents_df):
    print (f'Document: {documents_df.iloc[doc_id]["documents"]}')
    print ('\n')
    print (f'Similar Documents using {matrix}:')
    if matrix=='Cosine Similarity':
        similar_ix=np.argsort(similarity_matrix[doc_id])[::-1]
    elif matrix=='Euclidean Distance':
        similar_ix=np.argsort(similarity_matrix[doc_id])
    for ix in similar_ix:
        if ix==doc_id:
            continue
        print('\n')
        print (f'Document: {documents_df.iloc[ix]["documents"]}')
        print (f'{matrix} : {similarity_matrix[doc_id][ix]}')

def bert_cosine_similarity():
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    documents = ['Machine learning is the study of computer algorithms that improve automatically through experience.',
    'Machine learning is closely related to computational statistics, which focuses on making predictions using computers.',
    'Machine learning involves computers discovering how they can perform tasks without being explicitly programmed to do so.',
    'Machine learning approaches are traditionally divided into three broad categories, depending on the nature of the signal',
    'Software engineering is the systematic application of engineering approaches to the development of software',
    'A software engineer creates programs based on logic for the computer to execute. A software engineer has to be more concerned.'
    ]
    documents_df=pd.DataFrame(documents,columns=['documents'])
    stop_words_l=stopwords.words('english')
    documents_df['documents_cleaned']=documents_df.documents.apply(lambda x: " ".join(re.sub(r'[^a-zA-Z]',' ',w).lower() for w in x.split() if re.sub(r'[^a-zA-Z]',' ',w).lower() not in stop_words_l) )
    sentence_embeddings = sbert_model.encode(documents_df['documents_cleaned'])
    sentence_embeddings.shape
    pairwise_similarities=cosine_similarity(
        [sentence_embeddings[0]],
        sentence_embeddings[1:]
    )
    print(pairwise_similarities)
    #most_similar(0,pairwise_similarities,'Cosine Similarity')


def word_embedding_universal_sentence_encoder():
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4" 
    model = hub.load(module_url)
    print ("module %s loaded" % module_url)

    sentences = ["I went to eat to an italian restaurant.", 
       "We had a three-course meal.", 
       "Brad came to dinner with us.",
       "He loves fish tacos.",
       "In the end, we all felt like we ate too much.",
       "We all agreed; it was a magnificent evening."]

    query = "I had pizza and pasta."
    query_vec = model([query])[0]

    for sent in sentences:
        sim = cosine(query_vec, model([sent])[0])
        print(query, "and", sent, "has a similarity of:", sim)

def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

def obtain_comments():
    allComments=[]
    with open('reviewsHuaweiAppGallery.json') as a:
        json_object = json.load(a)
        for rev in json_object:
            allComments.append(rev['review'])

    return allComments



if __name__ == "__main__":
    list_comments = obtain_comments()
    word_mover_distance(list_comments)
    #bag_of_words_consine_similarity()
    #bert_cosine_similarity()
    #word_embedding_universal_sentence_encoder()