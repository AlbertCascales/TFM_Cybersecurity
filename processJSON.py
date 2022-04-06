#word mover distance
from cgitb import text
import logging
from pydoc import doc

from numpy import vectorize
from torch import combinations
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
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

#Read json file
import sys

def write_into_file(app1Name, app1Country, app1Author, app1Timestamp, app1Comment, app2Name, app2Country, app2Author, app2Timestamp, app2Comment):
    #open text file
    text_file = open("similar_reviews.txt", "a")
    
    #write string to file
    text_file.write("Application " + app1Name + " from " + app1Country + " with autor " + app1Author + " and date " + app1Timestamp + " and comment '" + app1Comment + "' is similar to " + "Application " + app2Name + " from " + app2Country + " with autor " + app2Author + " and date " + app2Timestamp + " and comment '" + app2Comment + "'")
    text_file.write('\n')
    #close file
    text_file.close()

def preprocess_word_mover_distance(sentence, stop_words):
    return [w for w in sentence.lower().split() if w not in stop_words]

#Word embedings (bag of words) + word mover distance
#Two identical sentences, have a value of 0
#Two completly different sentences have a value of 1.4 max
#1.1 could be a good value
def word_mover_distance(dictionary):

    download('stopwords')  # Download stopwords list.
    stop_words = stopwords.words('english')
    model = api.load('word2vec-google-news-300')
    model.init_sims(replace=True)

    for i in range(len(dictionary)):
        for j in range(i+1, len(dictionary)):
        
            comment1=dictionary[i]['review']
            comment2=dictionary[j]['review']

            first_sentence = preprocess_word_mover_distance(comment1, stop_words)
            second_sentence = preprocess_word_mover_distance(comment2, stop_words)

            distance = model.wmdistance(first_sentence, second_sentence)
            if (distance<=1.1):
                application1_name=dictionary[i]['application']
                application1_country=dictionary[i]['country']
                application1_author=dictionary[i]['author']
                application1_timestamp=dictionary[i]['timestamp']

                application2_name=dictionary[j]['application']
                application2_country=dictionary[j]['country']
                application2_author=dictionary[j]['author']
                application2_timestamp=dictionary[j]['timestamp']
                write_into_file(application1_name, application1_country, application1_author, application1_timestamp, comment1, application2_name, application2_country, application2_author, application2_timestamp, comment2)
            #print('The distance between', first_sentence, " and ", second_sentence, 'is', distance)

def preporcess_cosine_similarity(text):
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text =' '.join([word for word in text.split() if word not in stop_words])
    return text

def cosine_sim_vectors(vector1, vector2):
    vector1 = vector1.reshape(1, -1)
    vector2 = vector2.reshape(1, -1)
    return cosine_similarity(vector1, vector2)[0]

#Valor de 0 cuando son completamente diferentes y de 1 cuando son iguales
#0.2 parece un buen valor
def bag_of_words_consine_similarity(dictionary):

    comments_to_list=[]

    for i in range(len(dictionary)):

        comments_to_list.append(dictionary[i]['review'])

    """
    sentences = ["I ate dinner.", 
       "We had a three-course meal us.", 
       "Brad came to dinner with us.",
       "He loves fish tacos.",
       "In the end, we all felt like we ate too much.",
       "We all agreed; it was a magnificent evening."]
    """
    cleaned = list(map(preporcess_cosine_similarity, comments_to_list))
    #print(results)
    vectorizer = CountVectorizer().fit_transform(cleaned)
    vectors = vectorizer.toarray()
    #print(vectors)

    for i in range(len(comments_to_list)):
        for j in range(i+1, len(comments_to_list)):

            csim = cosine_sim_vectors(vectors[i], vectors[j])
            if (csim>0.1):
                application1_name=dictionary[i]['application']
                application1_country=dictionary[i]['country']
                application1_author=dictionary[i]['author']
                application1_timestamp=dictionary[i]['timestamp']

                application2_name=dictionary[j]['application']
                application2_country=dictionary[j]['country']
                application2_author=dictionary[j]['author']
                application2_timestamp=dictionary[j]['timestamp']
                write_into_file(application1_name, application1_country, application1_author, application1_timestamp, comments_to_list[i], application2_name, application2_country, application2_author, application2_timestamp, comments_to_list[j])
            
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

#Si son iguales vale 1, si son completamente distintos vale 0
def bert_cosine_similarity(dictionary):
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')

    comments_to_list=[]

    for i in range(len(dictionary)):

        comments_to_list.append(dictionary[i]['review'])

    """
    documents = ['Machine learning is the study of computer algorithms that improve automatically through experience.',
    'Machine learning is closely related to computational statistics, which focuses on making predictions using computers.',
    'Machine learning involves computers discovering how they can perform tasks without being explicitly programmed to do so.',
    'Machine learning approaches are traditionally divided into three broad categories, depending on the nature of the signal',
    'Software engineering is the systematic application of engineering approaches to the development of software',
    'A software engineer creates programs based on logic for the computer to execute. A software engineer has to be more concerned.'
    ]
    """
    documents_df=pd.DataFrame(comments_to_list,columns=['documents'])
    stop_words_l=stopwords.words('english')
    documents_df['documents_cleaned']=documents_df.documents.apply(lambda x: " ".join(re.sub(r'[^a-zA-Z]',' ',w).lower() for w in x.split() if re.sub(r'[^a-zA-Z]',' ',w).lower() not in stop_words_l) )
    sentence_embeddings = sbert_model.encode(documents_df['documents_cleaned'])
    sentence_embeddings.shape

    for i in range(len(comments_to_list)):
        linea=i
        print("Linea:",linea)

        pairwise_similarities=cosine_similarity(
            [sentence_embeddings[i]],
            sentence_embeddings[i+1:]
        )
        contador=1
        for a in pairwise_similarities:
            
            for elemento in a:
                elemento_analizado=linea+contador
                contador+=1

                print(elemento_analizado)
                
                if (elemento>0.5):
                    application1_name=dictionary[linea]['application']
                    application1_country=dictionary[linea]['country']
                    application1_author=dictionary[linea]['author']
                    application1_timestamp=dictionary[linea]['timestamp']
                    application2_name=dictionary[elemento_analizado]['application']
                    application2_country=dictionary[elemento_analizado]['country']
                    application2_author=dictionary[elemento_analizado]['author']
                    application2_timestamp=dictionary[elemento_analizado]['timestamp']
                    write_into_file(application1_name, application1_country, application1_author, application1_timestamp, comments_to_list[linea], application2_name, application2_country, application2_author, application2_timestamp, comments_to_list[elemento_analizado])
                
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
"""
def obtain_comments():
    allComments=[]
    with open('reviewsHuaweiAppGallery.json') as a:
        json_object = json.load(a)
        for rev in json_object:
            allComments.append(rev['review'])

    return allComments
"""




if __name__ == "__main__":
    #Read json file
    allComments =[]
    with open(sys.argv[1], "r") as json_file:
        json_object = json.load(json_file)
        for rev in json_object:
            #Save comments as list
            allComments.append(rev)

    #print(allComments[0]['review'])

    word_mover_distance(allComments)
    #bag_of_words_consine_similarity(allComments)
    #bert_cosine_similarity(allComments)
    #word_embedding_universal_sentence_encoder()