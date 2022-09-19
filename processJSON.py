#word mover distance
from cgitb import text
import logging
from pydoc import doc
from typing import KeysView

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
import chardet

#Read csv file
import csv
from csv import writer
from csv import DictWriter
import ast



listSimilarity=[]

def write_into_file(array):
    """
    text_file = open("similar_reviews_new.txt", "a")

    for element in array:
        text_file.write(element + "\n")

    text_file.close()

    listSimilarity.clear()
    """

    with open('similar_reviews_new.json', 'a', encoding='utf-8') as f:
        json.dump(array, f, ensure_ascii=False, indent=4)

    listSimilarity.clear()

def write_into_file_2(array):


    keys = array[0].keys()

    with open('similar_reviews_new.csv', 'a', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writerows(array)




    listSimilarity.clear()

def write_into_list(technique, storeApp1, app1Name, app1Country, app1Author, app1Timestamp, app1Comment, storeApp2, app2Name, app2Country, app2Author, app2Timestamp, app2Comment, value):
    #open text file
    #text_file = open("similar_reviews.txt", "a")
    
    #Check wired usernames
    stripped1= (c for c in app1Author if 0 < ord(c) < 127)
    app1Author=''.join(stripped1)
    stripped2 = (c for c in app2Author if 0 < ord(c) < 127)
    app2Author=''.join(stripped2)

    #check wired comments
    stripped1= (c for c in app1Comment if 0 < ord(c) < 127)
    app1Comment=''.join(stripped1)
    stripped2 = (c for c in app2Comment if 0 < ord(c) < 127)
    app2Comment=''.join(stripped2)

    similarity = {'Technique':technique, 'Store1':storeApp1,'Name1':app1Name,'Country1':app1Country,'Author1':app1Author,'Date1':app1Timestamp,'Comment1':app1Comment,'Store2':storeApp2,'Name2':app2Name,'Country2':app2Country,'Author2':app2Author,'Date2':app2Timestamp,'Comment2':app2Comment,'Similarity':str(value)}
    listSimilarity.append(similarity)

    #listSimilarity.append(technique + " : From store: " + storeApp1 + " the application " + app1Name + " from country " + app1Country + " with autor " + app1Author + " and date " + app1Timestamp + " and comment " + app1Comment + " is similar " + "from store " + storeApp2 +  " from application " + app2Name + " from country " + app2Country + " with autor " + app2Author + " and date " + app2Timestamp + " and comment " + app2Comment + "with a value of: " + str(value))
    #write string to file
    #text_file.write(technique + " : From store: " + storeApp1 + " the application " + app1Name + " from country " + app1Country + " with autor " + app1Author + " and date " + app1Timestamp + " and comment " + app1Comment + " is similar " + "from store " + storeApp2 +  " from application " + app2Name + " from country " + app2Country + " with autor " + app2Author + " and date " + app2Timestamp + " and comment " + app2Comment + "with a value of: " + str(value))
    #text_file.write('\n')
    #close file
    #text_file.close()

def preprocess_word_mover_distance(sentence, stop_words):
    return [w for w in sentence.lower().split() if w not in stop_words]

#Word embedings (bag of words) + word mover distance
#Two identical sentences, have a value of 0
#Two completly different sentences have a value of 1.4 max
#1.1 could be a good value
def word_mover_distance(dictionary):
    identiffier=1

    technique="word_mover_distance"

    download('stopwords')  # Download stopwords list.
    stop_words = stopwords.words('english')
    model = api.load('word2vec-google-news-300')
    model.init_sims(replace=True)

    for i in range(len(dictionary)):
        for j in range(i+1, len(dictionary)):
        
            comment1=dictionary[i]['review']
            comment2=dictionary[j]['review']

            try:

                word_list1 = comment1.split()
                number_of_words1 = len(word_list1)

                word_list2 = comment2.split()
                number_of_words2 = len(word_list2)

                if (number_of_words1>7 and number_of_words2>7):

                    first_sentence = preprocess_word_mover_distance(comment1, stop_words)
                    second_sentence = preprocess_word_mover_distance(comment2, stop_words)

                    distance = model.wmdistance(first_sentence, second_sentence)
                    print(distance)
                    if (distance<=1):
                        #print("Entra" + str(identiffier))
                        #identiffier+=1
                        application1_store=dictionary[i]['store']
                        application1_name=dictionary[i]['application']
                        application1_country=dictionary[i]['country']
                        application1_author=dictionary[i]['author']
                        application1_timestamp=dictionary[i]['timestamp']

                        application2_store=dictionary[j]['store']
                        application2_name=dictionary[j]['application']
                        application2_country=dictionary[j]['country']
                        application2_author=dictionary[j]['author']
                        application2_timestamp=dictionary[j]['timestamp']
                        write_into_list(technique, application1_store, application1_name, application1_country, application1_author, application1_timestamp, comment1,application2_store, application2_name, application2_country, application2_author, application2_timestamp, comment2, distance)
            except:
                pass

    write_into_file(listSimilarity)


def preporcess_cosine_similarity(text):
    if (text is not None):
        text = ''.join([word for word in text if word not in string.punctuation])
        if (text is not None):
            text = text.lower()
            if (text is not None):
                text =' '.join([word for word in text.split() if word not in stop_words])
                #print(text)
                return text
            else:
                return "a"
        else:
            return "a"
    else:
        return "a"


def cosine_sim_vectors(vector1, vector2):
    vector1 = vector1.reshape(1, -1)
    vector2 = vector2.reshape(1, -1)
    return cosine_similarity(vector1, vector2)[0]

#Valor de 0 cuando son completamente diferentes y de 1 cuando son iguales
def bag_of_words_consine_similarity(dictionary):

    technique="bag_of_words_cosine_similarity"

    comments_to_list=[]

    for i in range(len(dictionary)):
        comments_to_list.append(dictionary[i]['review'])

    iteracion=1

    try:

        cleaned = list(map(preporcess_cosine_similarity, comments_to_list))
        vectorizer = CountVectorizer().fit_transform(cleaned)
        vectors = vectorizer.toarray()
        #print(vectors)

        for i in range(len(comments_to_list)):
            for j in range(i+1, len(comments_to_list)):

                csim = cosine_sim_vectors(vectors[i], vectors[j])

                count1 = np.count_nonzero(vectors[i] == 1)
                count2 = np.count_nonzero(vectors[j] == 1)

                if (count1>7 and count2>7):
            
                    if (csim>0.3):
                        application1_store=dictionary[i]['store']
                        application1_name=dictionary[i]['application']
                        application1_country=dictionary[i]['country']
                        application1_author=dictionary[i]['author']
                        application1_timestamp=dictionary[i]['timestamp']

                        application2_store=dictionary[j]['store']
                        application2_name=dictionary[j]['application']
                        application2_country=dictionary[j]['country']
                        application2_author=dictionary[j]['author']
                        application2_timestamp=dictionary[j]['timestamp']
                        write_into_list(technique, application1_store, application1_name, application1_country, application1_author, application1_timestamp, comments_to_list[i], application2_store, application2_name, application2_country, application2_author, application2_timestamp, comments_to_list[j], csim)
                    
    except:
        pass

    write_into_file(listSimilarity)

def most_similar(technique, comments_to_list, similarity_matrix,documents_df, completeReview):

    numero=0

    keys=['Technique', 'Store1','Name1','Country1','Author1','Date1','Comment1','Store2','Name2','Country2','Author2','Date2','Comment2','Similarity']

    with open('similar_reviews_new.csv', 'a', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()

    for primero in range(len(comments_to_list)):
        for segundo in range(primero + 1, len(comments_to_list)):
            #print (f'{documents_df.iloc[primero]["documents"]} similar to {documents_df.iloc[segundo]["documents"]}  in {similarity_matrix[primero][segundo]}')
            word_list1 = documents_df.iloc[primero]["documents"].split()
            number_of_words1 = len(word_list1)

            word_list2 = documents_df.iloc[segundo]["documents"].split()
            number_of_words2 = len(word_list2)

            if (number_of_words1>7 and number_of_words2>7):

                if (similarity_matrix[primero][segundo] > 0.5):
                    
                    application1_store=completeReview[primero]['store']
                    application1_name=completeReview[primero]['application']
                    application1_country=completeReview[primero]['country']
                    application1_author=completeReview[primero]['author']
                    application1_timestamp=completeReview[primero]['timestamp']

                    application2_store=completeReview[segundo]['store']
                    application2_name=completeReview[segundo]['application']
                    application2_country=completeReview[segundo]['country']
                    application2_author=completeReview[segundo]['author']
                    application2_timestamp=completeReview[segundo]['timestamp']
                    write_into_list(technique, application1_store, application1_name, application1_country, application1_author, application1_timestamp, documents_df.iloc[primero]["documents"], application2_store, application2_name, application2_country, application2_author, application2_timestamp, documents_df.iloc[segundo]["documents"], similarity_matrix[primero][segundo])
                    
                    write_into_file_2(listSimilarity)


#Si son iguales vale 1, si son completamente distintos vale 0
def bert_cosine_similarity(dictionary):

    technique= "bert_cosine_similarity"

    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')

    comments_to_list=[]

    
    for i in range(len(dictionary)):

        if (dictionary[i]['review'] is not None):
            comments_to_list.append(dictionary[i]['review'])
    
    documents_df=pd.DataFrame(comments_to_list,columns=['documents'])
    stop_words_l=stopwords.words('english')
    documents_df['documents_cleaned']=documents_df.documents.apply(lambda x: " ".join(re.sub(r'[^a-zA-Z]',' ',w).lower() for w in x.split() if re.sub(r'[^a-zA-Z]',' ',w).lower() not in stop_words_l) )
    sentence_embeddings = sbert_model.encode(documents_df['documents_cleaned'])
    #print(sentence_embeddings)
    #sentence_embeddings.shape

    pairwise_similarities=cosine_similarity(sentence_embeddings)
    most_similar(technique, comments_to_list, pairwise_similarities, documents_df, dictionary)


#Vale -1 si no se parecen nada, y 1 si son idénticos
#0.3 puede ser un buen valor
def word_embedding_universal_sentence_encoder(dictionary):

    technique="word_embedding_universal_sentence_encoder"

    #module_url = "https://tfhub.dev/google/universal-sentence-encoder/4" 
    model = hub.load("C:\\Users\\marti\\Downloads\\universal-sentence-encoder_4")
    #print ("module %s loaded" % module_url)
    
    identiffier=1

    for i in range(len(dictionary)):
        for j in range(i+1, len(dictionary)):

            comment1=dictionary[i]['review']
            comment2=dictionary[j]['review']
        
            if (comment1 is not None and comment2 is not None):

                word_list1 = comment1.split()
                number_of_words1 = len(word_list1)

                word_list2 = comment2.split()
                number_of_words2 = len(word_list2)

                if (number_of_words1>7 or number_of_words2>7):
                
            
                    reference = model([comment1])[0]
                    comparation=model([comment2])[0]

                    #for sent in sentences:
                    sim = cosine(reference, comparation)
                    if (sim>0.7):
                        print("Entra" + str(identiffier))
                        identiffier+=1
                        application1_store=dictionary[i]['store']
                        application1_name=dictionary[i]['application']
                        application1_country=dictionary[i]['country']
                        application1_author=dictionary[i]['author']
                        application1_timestamp=dictionary[i]['timestamp']

                        application2_store=dictionary[j]['store']
                        application2_name=dictionary[j]['application']
                        application2_country=dictionary[j]['country']
                        application2_author=dictionary[j]['author']
                        application2_timestamp=dictionary[j]['timestamp']
                        write_into_list(technique, application1_store, application1_name, application1_country, application1_author, application1_timestamp, comment1, application2_store, application2_name, application2_country, application2_author, application2_timestamp, comment2, sim)
                        write_into_file(listSimilarity)

                    #print(comment1, "and", comment2, "has a similarity of:", sim)

    #write_into_file(listSimilarity)


def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))




if __name__ == "__main__":
    #Read json file
    allComments =[]
    with open(sys.argv[1],  'r', encoding='utf-8') as json_file:
        json_object = json.load(json_file)
        for rev in json_object:
            #Save comments as list
            allComments.append(rev)

    #print(allComments[0]['review'])

    #word_mover_distance(allComments)
    #print("segundo")
    #bag_of_words_consine_similarity(allComments)
    #print("tercero")
    bert_cosine_similarity(allComments)
    #print("terminado")
    #word_embedding_universal_sentence_encoder(allComments)