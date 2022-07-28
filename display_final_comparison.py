import json
import sys

listSameReviews=[]

def write_into_file(array):

    with open('same_reviews_three_models.json', 'a', encoding='utf-8') as f:
        json.dump(array, f, ensure_ascii=False, indent=4)

    listSameReviews.clear()

def write_into_list(technique1_technique, technique1_store1, technique1_name1, technique1_country1, technique1_author1, technique1_timestamp1, technique1_store2,technique1_name2, technique1_country2, technique1_author2, technique1_timestamp2, technique1_similarity,technique1_comment1, technique1_comment2, technique2_technique, technique2_store1, technique2_name1, technique2_country1, technique2_author1, technique2_timestamp1, technique2_store2,technique2_name2, technique2_country2, technique2_author2, technique2_timestamp2, technique2_similarity, technique2_comment1, technique2_comment2, technique3_technique, technique3_store1, technique3_name1, technique3_country1, technique3_author1, technique3_timestamp1, technique3_store2,technique3_name2, technique3_country2, technique3_author2, technique3_timestamp2, technique3_similarity, technique3_comment1, technique3_comment2,):
    
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

    similarity = {'Tech1Technique':technique1_technique, 'Tech1Store1':technique1_store1,'Tech1AppName1':technique1_name1,'Tech1Country1':technique1_country1,'Tech1Author1':tech1Author1,'Tech1Date1':technique1_timestamp1, 'Tech1Store2':technique1_store2,'Tech1AppName2':technique1_name2,'Tech1Country2':technique1_country2,'Tech1Author2':tech1Author2,'Tech1Date2':technique1_timestamp2,'Tech1Similarity':str(technique1_similarity), 'Tech1Comment1':tech1Comment1, 'Tech1Comment2': tech1Comment2, 
    'Tech2Technique':technique2_technique,'Tech2Store1':technique2_store1,'Tech2AppName1':technique2_name1,'Tech2Country1':technique2_country1,'Tech2Author1':tech2Author1,'Tech2Date1':technique2_timestamp1, 'Tech2Store2':technique2_store2,'Tech2AppName2':technique2_name2,'Tech2Country2':technique2_country2,'Tech2Author2':tech2Author2,'Tech2Date2':technique2_timestamp2,'Tech2Similarity':str(technique2_similarity), 'Tech2Comment1':tech2Comment1, 'Tech2Comment2': tech2Comment2,
    'Tech3Technique':technique3_technique, 'Tech3Store1':technique3_store1,'Tech3AppName1':technique3_name1,'Tech3Country1':technique3_country1,'Tech3Author1':tech3Author1,'Tech3Date1':technique3_timestamp1, 'Tech3Store2':technique3_store2,'Tech3AppName2':technique3_name2,'Tech3Country2':technique3_country2,'Tech3Author2':tech3Author2,'Tech3Date2':technique3_timestamp2,'Tech3Similarity':str(technique3_similarity), 'Tech3Comment1':tech3Comment1, 'Tech3Comment2': tech3Comment2}
    
    listSameReviews.append(similarity)

def compare_models_preprocessed():

    numero=1

    with open(sys.argv[1],  'r', encoding='utf-8') as json_file1, open(sys.argv[2],  'r', encoding='utf-8') as json_file2:
        first_models = json.load(json_file1)
        second_models = json.load(json_file2)

        for reviews_first_models in first_models:
            comment1_reviews_first_models = reviews_first_models['Tech1Comment1']
            comment2_reviews_first_models = reviews_first_models['Tech1Comment2']    
            for reviews_second_models in second_models:
                comment1_second_models = reviews_second_models['Tech1Comment1']
                comment2_second_models = reviews_second_models['Tech1Comment2']
                
            
                if (((comment1_reviews_first_models==comment1_second_models) and (comment2_reviews_first_models==comment2_second_models)) or
                    ((comment1_reviews_first_models==comment2_second_models) and (comment2_reviews_first_models==comment1_second_models))):

                    bagOfWords_technique='Bag_of_words'
                    bagOfWords_store1=reviews_first_models['Tech1Store1']
                    bagOfWords_name1=reviews_first_models['Tech1AppName1']
                    bagOfWords_country1=reviews_first_models['Tech1Country1']
                    bagOfWords_author1=reviews_first_models['Tech1Author1']
                    bagOfWords_timestamp1=reviews_first_models['Tech1Date1']
                    bagOfWords_store2=reviews_first_models['Tech1Store2']
                    bagOfWords_name2=reviews_first_models['Tech1AppName2']
                    bagOfWords_country2=reviews_first_models['Tech1Country2']
                    bagOfWords_author2=reviews_first_models['Tech1Author2']
                    bagOfWords_timestamp2=reviews_first_models['Tech1Date2']
                    bagOfWords_similarity=reviews_first_models['Tech1Similarity']
                    bagOfWords_comment1=reviews_first_models['Tech1Comment1']
                    bagOfWords_comment2=reviews_first_models['Tech1Comment2']

                    Bert_technique="Bert"
                    Bert_store1=reviews_first_models['Tech2Store1']
                    Bert_name1=reviews_first_models['Tech2AppName1']
                    Bert_country1=reviews_first_models['Tech2Country1']
                    Bert_author1=reviews_first_models['Tech2Author1']
                    Bert_timestamp1=reviews_first_models['Tech2Date1']
                    Bert_store2=reviews_first_models['Tech2Store2']
                    Bert_name2=reviews_first_models['Tech2AppName2']
                    Bert_country2=reviews_first_models['Tech2Country2']
                    Bert_author2=reviews_first_models['Tech2Author2']
                    Bert_timestamp2=reviews_first_models['Tech2Date2']
                    Bert_similarity=reviews_first_models['Tech2Similarity']
                    Bert_comment1=reviews_first_models['Tech2Comment1']
                    Bert_comment2=reviews_first_models['Tech2Comment2']

                    WMD_technique="WMD"
                    WMD_store1=reviews_second_models['Tech2Store1']
                    WMD_name1=reviews_second_models['Tech2AppName1']
                    WMD_country1=reviews_second_models['Tech2Country1']
                    WMD_author1=reviews_second_models['Tech2Author1']
                    WMD_timestamp1=reviews_second_models['Tech2Date1']
                    WMD_store2=reviews_second_models['Tech2Store2']
                    WMD_name2=reviews_second_models['Tech2AppName2']
                    WMD_country2=reviews_second_models['Tech2Country2']
                    WMD_author2=reviews_second_models['Tech2Author2']
                    WMD_timestamp2=reviews_second_models['Tech2Date2']
                    WMD_similarity=reviews_second_models['Tech2Similarity']
                    WMD_comment1=reviews_second_models['Tech2Comment1']
                    WMD_comment2=reviews_second_models['Tech2Comment2']

                    write_into_list(bagOfWords_technique, bagOfWords_store1, bagOfWords_name1, bagOfWords_country1, bagOfWords_author1, bagOfWords_timestamp1, bagOfWords_store2,bagOfWords_name2, bagOfWords_country2, bagOfWords_author2, bagOfWords_timestamp2, bagOfWords_similarity,bagOfWords_comment1, bagOfWords_comment2,
                    Bert_technique, Bert_store1, Bert_name1, Bert_country1, Bert_author1, Bert_timestamp1, Bert_store2,Bert_name2, Bert_country2, Bert_author2, Bert_timestamp2, Bert_similarity, Bert_comment1 , Bert_comment2,
                    WMD_technique, WMD_store1, WMD_name1, WMD_country1, WMD_author1, WMD_timestamp1, WMD_store2,WMD_name2, WMD_country2, WMD_author2, WMD_timestamp2, WMD_similarity, WMD_comment1 , WMD_comment2)
                    
                    print("Entra"+str(numero))
                    numero+=1
        write_into_file(listSameReviews) 

if __name__ == "__main__":

    compare_models_preprocessed()