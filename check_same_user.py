from itertools import count
import json, sys
from xml.dom.minidom import Identified
from nltk.corpus import stopwords
from nltk import download
from difflib import SequenceMatcher
import string

listSameReviews=[]
authorDictionary=[]

def write_into_file(array):

    with open('identical_review.json', 'a', encoding='utf-8') as f:
        json.dump(array, f, ensure_ascii=False, indent=4)

    #listSameReviews.clear()
    authorDictionary.clear()

def write_into_list(country, store, author, timestamp, comment):
    
    #Check wired usernames
    stripped1= (c for c in author if 0 < ord(c) < 127)
    author_cleaned=''.join(stripped1)
    

    #check wired comments
    stripped1= (c for c in comment if 0 < ord(c) < 127)
    comment_cleaned=''.join(stripped1)
    

    """
    similarity = {'Tech1Technique':technique1_technique, 'Tech1Store1':technique1_store1,'Tech1AppName1':technique1_name1,'Tech1Country1':technique1_country1,'Tech1Author1':tech1Author1,'Tech1Date1':technique1_timestamp1, 'Tech1Store2':technique1_store2,'Tech1AppName2':technique1_name2,'Tech1Country2':technique1_country2,'Tech1Author2':tech1Author2,'Tech1Date2':technique1_timestamp2,'Tech1Similarity':str(technique1_similarity), 'Tech1Comment1':tech1Comment1, 'Tech1Comment2': tech1Comment2, 
    'Tech2Technique':technique2_technique,'Tech2Store1':technique2_store1,'Tech2AppName1':technique2_name1,'Tech2Country1':technique2_country1,'Tech2Author1':tech2Author1,'Tech2Date1':technique2_timestamp1, 'Tech2Store2':technique2_store2,'Tech2AppName2':technique2_name2,'Tech2Country2':technique2_country2,'Tech2Author2':tech2Author2,'Tech2Date2':technique2_timestamp2,'Tech2Similarity':str(technique2_similarity), 'Tech2Comment1':tech2Comment1, 'Tech2Comment2': tech2Comment2,
    'Tech3Technique':technique3_technique, 'Tech3Store1':technique3_store1,'Tech3AppName1':technique3_name1,'Tech3Country1':technique3_country1,'Tech3Author1':tech3Author1,'Tech3Date1':technique3_timestamp1, 'Tech3Store2':technique3_store2,'Tech3AppName2':technique3_name2,'Tech3Country2':technique3_country2,'Tech3Author2':tech3Author2,'Tech3Date2':technique3_timestamp2,'Tech3Similarity':str(technique3_similarity), 'Tech3Comment1':tech3Comment1, 'Tech3Comment2': tech3Comment2}
    listSameReviews.append(similarity)
    """
    

    dictionary={'Country': country, 'Application':store, 'Author':author_cleaned, 'Date':timestamp, 'Comment':comment_cleaned}

    authorDictionary.append(dictionary)

    


def preprocess_word_mover_distance(sentence, stop_words):
    return [w for w in sentence.lower().split() if w not in stop_words]

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def check_identical_reviews():
    contador=0
    with open(sys.argv[1],  'r', encoding='utf-8') as json_file1:
        pair_reviews = json.load(json_file1)
        download('stopwords')  # Download stopwords list.
        stop_words = stopwords.words('english')

        for review in pair_reviews:
            comment1 = review['Tech1Comment1']
            comment2 = review['Tech1Comment2']

            first_review = preprocess_word_mover_distance(comment1, stop_words)
            second_review = preprocess_word_mover_distance(comment2, stop_words)

            first_comment=' '.join(first_review)
            second_comment=' '.join(second_review)

            if similar(first_comment,second_comment)>0.75:
                bagOfWords_technique='Bag_of_words'
                bagOfWords_store1=review['Tech1Store1']
                bagOfWords_name1=review['Tech1AppName1']
                bagOfWords_country1=review['Tech1Country1']
                bagOfWords_author1=review['Tech1Author1']
                bagOfWords_timestamp1=review['Tech1Date1']
                bagOfWords_store2=review['Tech1Store2']
                bagOfWords_name2=review['Tech1AppName2']
                bagOfWords_country2=review['Tech1Country2']
                bagOfWords_author2=review['Tech1Author2']
                bagOfWords_timestamp2=review['Tech1Date2']
                bagOfWords_similarity=review['Tech1Similarity']
                bagOfWords_comment1=review['Tech1Comment1']
                bagOfWords_comment2=review['Tech1Comment2']

                Bert_technique="Bert"
                Bert_store1=review['Tech2Store1']
                Bert_name1=review['Tech2AppName1']
                Bert_country1=review['Tech2Country1']
                Bert_author1=review['Tech2Author1']
                Bert_timestamp1=review['Tech2Date1']
                Bert_store2=review['Tech2Store2']
                Bert_name2=review['Tech2AppName2']
                Bert_country2=review['Tech2Country2']
                Bert_author2=review['Tech2Author2']
                Bert_timestamp2=review['Tech2Date2']
                Bert_similarity=review['Tech2Similarity']
                Bert_comment1=review['Tech2Comment1']
                Bert_comment2=review['Tech2Comment2']

                WMD_technique="WMD"
                WMD_store1=review['Tech2Store1']
                WMD_name1=review['Tech2AppName1']
                WMD_country1=review['Tech2Country1']
                WMD_author1=review['Tech2Author1']
                WMD_timestamp1=review['Tech2Date1']
                WMD_store2=review['Tech2Store2']
                WMD_name2=review['Tech2AppName2']
                WMD_country2=review['Tech2Country2']
                WMD_author2=review['Tech2Author2']
                WMD_timestamp2=review['Tech2Date2']
                WMD_similarity=review['Tech2Similarity']
                WMD_comment1=review['Tech2Comment1']
                WMD_comment2=review['Tech2Comment2']

                write_into_list(bagOfWords_country1, bagOfWords_name1, bagOfWords_author1, bagOfWords_timestamp1, bagOfWords_comment1)
                write_into_list(bagOfWords_country2, bagOfWords_name2, bagOfWords_author2, bagOfWords_timestamp2, bagOfWords_comment2)
                write_into_list(Bert_country1, Bert_name1 ,Bert_author1, Bert_timestamp1, Bert_comment1)
                write_into_list(Bert_country2, Bert_name2 ,Bert_author2, Bert_timestamp2, Bert_comment2)
                write_into_list(WMD_country1, WMD_name1, WMD_author1, WMD_timestamp1, WMD_comment1)
                write_into_list(WMD_country2, WMD_name2, WMD_author2, WMD_timestamp2, WMD_comment2)
                    


        #write_into_file(listSameReviews) 
        write_into_file(authorDictionary)

def check_same_users():

    k_v_exchanged = {}
    valor=""

    with open("identical_review.json",  'r', encoding='utf-8') as json_file1:
        identical_reviews = json.load(json_file1)

        for review in identical_reviews:
            Author=review["Author"]
            Date=review["Date"]
            Comment=review["Comment"]

            
            if Author not in dictionary:

                valor="'Author':Author"

                dictionary["Author"].append(Author)
                dictionary["Date"].append(Date)
                dictionary["Comment"].append(Comment)

                """
                k_v_exchanged[Author] = 1
                k_v_exchanged[Date] = Date
                k_v_exchanged[Comment] = Comment
                """
            else:
                print("esta")
                """
                date_old = dictionary.get("Date")
                comment_old = dictionary.get("Comment")
                author_old=dictionary.get(Author)

                if (date_old==Date and comment_old==Comment):
                    k_v_exchanged[Author] = author_old+1

                else:
                    k_v_exchanged[Author] = 1
                    k_v_exchanged[Date] = Date
                    k_v_exchanged[Comment] = Comment

    repeated_authors = {key:val for key, val in k_v_exchanged.items() if val != 1}

    for key, value in k_v_exchanged.items():
        print(key, ":", value)
        """

        print(dictionary)

def remove_duplicates():
    with open("identical_review.json",  'r', encoding='utf-8') as json_file1:
        identical_reviews = json.load(json_file1)

        seen = []
        for x in identical_reviews:
            print(x)
            if x not in seen:
                seen.append(x)

    with open('identical_review_without_duplicates.json', 'a', encoding='utf-8') as f:
        json.dump(seen, f, ensure_ascii=False, indent=4)

    seen.clear()

if __name__ == "__main__":

    check_identical_reviews()

    remove_duplicates()

    #check_same_users()