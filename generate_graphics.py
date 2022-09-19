import sys, json, collections
from collections import Counter
from unicodedata import name
import matplotlib.pyplot as plt
import numpy as np

topic_list=[]

def generate_porcentajes():
    yes_count=0
    total_count=0

    with open(sys.argv[1],  'r', encoding='utf-8') as json_file1:
        manual_processed = json.load(json_file1)

        for reviews in manual_processed:
            yes_output = reviews['Manual']
            topic_list.append(reviews['Topic'])
            if (yes_output=="Yes"):
                yes_count+=1
            total_count+=1

        print(yes_count , "of" , total_count)
        print("Accuracy:" , (yes_count/total_count)*100)
        
        dictionary = Counter(topic_list)
        

        ship = collections.OrderedDict(dictionary)
        lists = sorted(dictionary.items(), key=lambda kv: kv[1], reverse=True)
        x, y = zip(*lists) # unpack a list of pairs into two tuples
        plt.ylabel('Number of occurrences')
        plt.title('Topics of similar reviews')
        plt.xticks(range(len(x)), x, rotation=90)
        plt.bar(x, y)
        plt.show()


        





if __name__ == "__main__":

    generate_porcentajes()