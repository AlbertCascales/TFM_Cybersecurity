import sys
import json
import csv
import pandas as pd
import ijson
import time

csvFile="similar_reviews_bert_cosine_similarity.csv"
jsonFile="similar_reviews_bert_cosine_similarity.json"
listCSV=[]

listSameReviews=[]
allComments=[]

def convertir_csv_to_json():
    #Convert csv to json


    with open(csvFile) as csvf: 
        #load csv file data using csv library's dictionary reader
        csvReader = csv.DictReader(csvf) 

        #convert each csv row into python dict
        for row in csvReader:
            #add this python dict to json array
            listCSV.append(row)

    #convert python jsonArray to JSON String and write to file
    with open(jsonFile, 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(listCSV, indent=4)
        jsonf.write(jsonString)

def write_into_file(array):

    with open('same_reviews_two_models.json', 'a', encoding='utf-8') as f:
        json.dump(array, f, ensure_ascii=False, indent=4)

    listSameReviews.clear()

def write_into_list(technique1_store1, technique1_name1, technique1_country1, technique1_author1, technique1_timestamp1, technique1_store2,technique1_name2, technique1_country2, technique1_author2, technique1_timestamp2, technique1_similarity,technique1_comment1, technique1_comment2, technique2_store1, technique2_name1, technique2_country1, technique2_author1, technique2_timestamp1, technique2_store2,technique2_name2, technique2_country2, technique2_author2, technique2_timestamp2, technique2_similarity, technique2_comment1, technique2_comment2, technique3_store1, technique3_name1, technique3_country1, technique3_author1, technique3_timestamp1, technique3_store2,technique3_name2, technique3_country2, technique3_author2, technique3_timestamp2, technique3_similarity, technique3_comment1, technique3_comment2,):
    
    #Check wired usernames
    stripped1= (c for c in technique1_author1 if 0 < ord(c) < 127)
    tech1Author1=''.join(stripped1)
    stripped2 = (c for c in technique1_author2 if 0 < ord(c) < 127)
    tech1Author2=''.join(stripped2)
    stripped3= (c for c in technique2_author1 if 0 < ord(c) < 127)
    tech2Author1=''.join(stripped3)
    stripped4 = (c for c in technique2_author2 if 0 < ord(c) < 127)
    tech2Author2=''.join(stripped4)
    stripped5= (c for c in technique3_author1 if 0 < ord(c) < 127)
    tech3Author1=''.join(stripped5)
    stripped6 = (c for c in technique3_author2 if 0 < ord(c) < 127)
    tech3Author2=''.join(stripped6)

    #check wired comments
    stripped1= (c for c in technique1_comment1 if 0 < ord(c) < 127)
    tech1Comment1=''.join(stripped1)
    stripped2 = (c for c in technique1_comment2 if 0 < ord(c) < 127)
    tech1Comment2=''.join(stripped2)
    stripped3= (c for c in technique2_comment1 if 0 < ord(c) < 127)
    tech2Comment1=''.join(stripped3)
    stripped4 = (c for c in technique2_comment2 if 0 < ord(c) < 127)
    tech2Comment2=''.join(stripped4)
    stripped5= (c for c in technique3_comment1 if 0 < ord(c) < 127)
    tech3Comment1=''.join(stripped5)
    stripped6 = (c for c in technique3_comment2 if 0 < ord(c) < 127)
    tech3Comment2=''.join(stripped6)

    similarity = {'Tech1Store1':technique1_store1,'Tech1AppName1':technique1_name1,'Tech1Country1':technique1_country1,'Tech1Author1':tech1Author1,'Tech1Date1':technique1_timestamp1, 'Tech1Store2':technique1_store2,'Tech1AppName2':technique1_name2,'Tech1Country2':technique1_country2,'Tech1Author2':tech1Author2,'Tech1Date2':technique1_timestamp2,'Tech1Similarity':str(technique1_similarity), 'Tech1Comment1':tech1Comment1, 'Tech1Comment2': tech1Comment2, 
    'Tech2Store1':technique2_store1,'Tech2AppName1':technique2_name1,'Tech2Country1':technique2_country1,'Tech2Author1':tech2Author1,'Tech2Date1':technique2_timestamp1, 'Tech2Store2':technique2_store2,'Tech2AppName2':technique2_name2,'Tech2Country2':technique2_country2,'Tech2Author2':tech2Author2,'Tech2Date2':technique2_timestamp2,'Tech2Similarity':str(technique2_similarity), 'Tech2Comment1':tech2Comment1, 'Tech2Comment2': tech2Comment2,
    'Tech3Store1':technique3_store1,'Tech3AppName1':technique3_name1,'Tech3Country1':technique3_country1,'Tech3Author1':tech3Author1,'Tech3Date1':technique3_timestamp1, 'Tech3Store2':technique3_store2,'Tech3AppName2':technique3_name2,'Tech3Country2':technique3_country2,'Tech3Author2':tech3Author2,'Tech3Date2':technique3_timestamp2,'Tech3Similarity':str(technique3_similarity), 'Tech3Comment1':tech3Comment1, 'Tech3Comment2': tech3Comment2}
    listSameReviews.append(similarity)

def write_into_list2(technique1_store1, technique1_name1, technique1_country1, technique1_author1, technique1_timestamp1, technique1_store2,technique1_name2, technique1_country2, technique1_author2, technique1_timestamp2, technique1_similarity,technique1_comment1, technique1_comment2, technique2_store1, technique2_name1, technique2_country1, technique2_author1, technique2_timestamp1, technique2_store2,technique2_name2, technique2_country2, technique2_author2, technique2_timestamp2, technique2_similarity, technique2_comment1, technique2_comment2):
    #Check wired usernames
    stripped1= (c for c in technique1_author1 if 0 < ord(c) < 127)
    tech1Author1=''.join(stripped1)
    stripped2 = (c for c in technique1_author2 if 0 < ord(c) < 127)
    tech1Author2=''.join(stripped2)
    stripped3= (c for c in technique2_author1 if 0 < ord(c) < 127)
    tech2Author1=''.join(stripped3)
    stripped4 = (c for c in technique2_author2 if 0 < ord(c) < 127)
    tech2Author2=''.join(stripped4)

    #check wired comments
    stripped1= (c for c in technique1_comment1 if 0 < ord(c) < 127)
    tech1Comment1=''.join(stripped1)
    stripped2 = (c for c in technique1_comment2 if 0 < ord(c) < 127)
    tech1Comment2=''.join(stripped2)
    stripped3= (c for c in technique2_comment1 if 0 < ord(c) < 127)
    tech2Comment1=''.join(stripped3)
    stripped4 = (c for c in technique2_comment2 if 0 < ord(c) < 127)
    tech2Comment2=''.join(stripped4)

    similarity = {'Tech1Store1':technique1_store1,'Tech1AppName1':technique1_name1,'Tech1Country1':technique1_country1,'Tech1Author1':tech1Author1,'Tech1Date1':technique1_timestamp1, 'Tech1Store2':technique1_store2,'Tech1AppName2':technique1_name2,'Tech1Country2':technique1_country2,'Tech1Author2':tech1Author2,'Tech1Date2':technique1_timestamp2,'Tech1Similarity':str(technique1_similarity), 'Tech1Comment1':tech1Comment1, 'Tech1Comment2': tech1Comment2, 
    'Tech2Store1':technique2_store1,'Tech2AppName1':technique2_name1,'Tech2Country1':technique2_country1,'Tech2Author1':tech2Author1,'Tech2Date1':technique2_timestamp1, 'Tech2Store2':technique2_store2,'Tech2AppName2':technique2_name2,'Tech2Country2':technique2_country2,'Tech2Author2':tech2Author2,'Tech2Date2':technique2_timestamp2,'Tech2Similarity':str(technique2_similarity), 'Tech2Comment1':tech2Comment1, 'Tech2Comment2': tech2Comment2}
    listSameReviews.append(similarity)

def compare_models():
    numero=1

    with open(sys.argv[1],  'r', encoding='utf-8') as json_file1, open(sys.argv[2],  'r', encoding='utf-8') as json_file2:
        bag_of_words = json.load(json_file1)
        bert_cosine_similarity = json.load(json_file2)
        #word_mover_distance = json.load(json_file3)
        
        for reviews_similar_bag_of_words in bag_of_words:
            comment1_bag_of_words = reviews_similar_bag_of_words['Comment1']
            comment2_bag_of_words = reviews_similar_bag_of_words['Comment2']    
            for reviews_similar_bert_cosine_similarity in bert_cosine_similarity:
                comment1_bert_cosine_similarity = reviews_similar_bert_cosine_similarity['Comment1']
                comment2_bert_cosine_similarity = reviews_similar_bert_cosine_similarity['Comment2']
                #for reviews_similar_word_mover_distance in word_mover_distance:
                #    comment1_word_mover_distance = reviews_similar_word_mover_distance['Comment1']
                #    comment2_word_mover_distance = reviews_similar_word_mover_distance['Comment2']
                    
                """
                    if  (((comment1_bag_of_words==comment1_bert_cosine_similarity==comment1_word_mover_distance) and (comment2_bag_of_words==comment2_bert_cosine_similarity==comment2_word_mover_distance)) or 
                        ((comment1_bag_of_words==comment1_bert_cosine_similarity==comment2_word_mover_distance) and (comment2_bag_of_words==comment2_bert_cosine_similarity==comment1_word_mover_distance)) or
                        ((comment1_bag_of_words==comment2_bert_cosine_similarity==comment1_word_mover_distance) and (comment2_bag_of_words==comment1_bert_cosine_similarity==comment2_word_mover_distance)) or
                        ((comment1_bag_of_words==comment2_bert_cosine_similarity==comment2_word_mover_distance) and (comment2_bag_of_words==comment1_bert_cosine_similarity==comment1_word_mover_distance))):    
                """

                if (((comment1_bag_of_words==comment1_bert_cosine_similarity) and (comment2_bag_of_words==comment2_bert_cosine_similarity)) or
                    ((comment1_bag_of_words==comment2_bert_cosine_similarity) and (comment2_bag_of_words==comment1_bert_cosine_similarity))):

                    technique1_store1=reviews_similar_bag_of_words['Store1']
                    technique1_name1=reviews_similar_bag_of_words['Name1']
                    technique1_country1=reviews_similar_bag_of_words['Country1']
                    technique1_author1=reviews_similar_bag_of_words['Author1']
                    technique1_timestamp1=reviews_similar_bag_of_words['Date1']
                    technique1_store2=reviews_similar_bag_of_words['Store2']
                    technique1_name2=reviews_similar_bag_of_words['Name2']
                    technique1_country2=reviews_similar_bag_of_words['Country2']
                    technique1_author2=reviews_similar_bag_of_words['Author2']
                    technique1_timestamp2=reviews_similar_bag_of_words['Date2']
                    technique1_similarity=reviews_similar_bag_of_words['Similarity']
                    technique1_comment1=reviews_similar_bag_of_words['Comment1']
                    technique1_comment2=reviews_similar_bag_of_words['Comment2']

                    technique2_store1=reviews_similar_bert_cosine_similarity['Store1']
                    technique2_name1=reviews_similar_bert_cosine_similarity['Name1']
                    technique2_country1=reviews_similar_bert_cosine_similarity['Country1']
                    technique2_author1=reviews_similar_bert_cosine_similarity['Author1']
                    technique2_timestamp1=reviews_similar_bert_cosine_similarity['Date1']
                    technique2_store2=reviews_similar_bert_cosine_similarity['Store2']
                    technique2_name2=reviews_similar_bert_cosine_similarity['Name2']
                    technique2_country2=reviews_similar_bert_cosine_similarity['Country2']
                    technique2_author2=reviews_similar_bert_cosine_similarity['Author2']
                    technique2_timestamp2=reviews_similar_bert_cosine_similarity['Date2']
                    technique2_similarity=reviews_similar_bert_cosine_similarity['Similarity']
                    technique2_comment1=reviews_similar_bert_cosine_similarity['Comment1']
                    technique2_comment2=reviews_similar_bert_cosine_similarity['Comment2']

                    """
                    technique3_store1=reviews_similar_word_mover_distance['Store1']
                    technique3_name1=reviews_similar_word_mover_distance['Name1']
                    technique3_country1=reviews_similar_word_mover_distance['Country1']
                    technique3_author1=reviews_similar_word_mover_distance['Author1']
                    technique3_timestamp1=reviews_similar_word_mover_distance['Date1']
                    technique3_store2=reviews_similar_word_mover_distance['Store2']
                    technique3_name2=reviews_similar_word_mover_distance['Name2']
                    technique3_country2=reviews_similar_word_mover_distance['Country2']
                    technique3_author2=reviews_similar_word_mover_distance['Author2']
                    technique3_timestamp2=reviews_similar_word_mover_distance['Date2']
                    technique3_similarity=reviews_similar_word_mover_distance['Similarity']
                    technique3_comment1=reviews_similar_word_mover_distance['Comment1']
                    technique3_comment2=reviews_similar_word_mover_distance['Comment2']
                    """
                    
                    #allComments.append(comment1_bag_of_words, comment2_bag_of_words, comment1_bert_cosine_similarity, comment2_bert_cosine_similarity, comment1_word_mover_distance, comment2_word_mover_distance)
                    #allComments = list(set(allComments))

                    """
                    write_into_list(technique1_store1, technique1_name1, technique1_country1, technique1_author1, technique1_timestamp1, technique1_store2,technique1_name2, technique1_country2, technique1_author2, technique1_timestamp2, technique1_similarity,technique1_comment1, technique1_comment2,
                    technique2_store1, technique2_name1, technique2_country1, technique2_author1, technique2_timestamp1, technique2_store2,technique2_name2, technique2_country2, technique2_author2, technique2_timestamp2, technique2_similarity, technique2_comment1 , technique2_comment2,
                    technique3_store1, technique3_name1, technique3_country1, technique3_author1, technique3_timestamp1, technique3_store2,technique3_name2, technique3_country2, technique3_author2, technique3_timestamp2, technique3_similarity, technique3_comment1 , technique3_comment2)
                    """
                    write_into_list2(technique1_store1, technique1_name1, technique1_country1, technique1_author1, technique1_timestamp1, technique1_store2,technique1_name2, technique1_country2, technique1_author2, technique1_timestamp2, technique1_similarity,technique1_comment1, technique1_comment2,
                    technique2_store1, technique2_name1, technique2_country1, technique2_author1, technique2_timestamp1, technique2_store2,technique2_name2, technique2_country2, technique2_author2, technique2_timestamp2, technique2_similarity, technique2_comment1 , technique2_comment2)
                    
                    print("Entra"+str(numero))
                    numero+=1

        write_into_file(listSameReviews)         

if __name__ == "__main__":

    #convertir_csv_to_json()

    compare_models()