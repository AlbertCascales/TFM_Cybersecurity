import json

newMoverDistance=[]
numero=1

with open("similar_reviews_wordMoverDistance.json", "r") as read_file:
    data = json.load(read_file)
    for comment in data:
        length_comment1 = len(comment['Comment1'])
        length_comment2 = len(comment['Comment2'])
        similarity = comment['Similarity']

        if (length_comment1>7 and length_comment2>7 and float(similarity)<0.8):
            print(numero)
            numero+=1
            newMoverDistance.append(comment)

    with open('reduced_similar_reviews_wordMoverDistance.json', 'a', encoding='utf-8') as f:
        json.dump(newMoverDistance, f, ensure_ascii=False, indent=4)

    newMoverDistance.clear()
