import json
from deep_translator import GoogleTranslator

langs_dict = GoogleTranslator.get_supported_languages(as_dict=True)  # output: {arabic: ar, french: fr, english:en etc...}
print(langs_dict)
 
"""
# Opening JSON file
f = open('reviewsGooglePlay.json', 'r')
 
# returns JSON object as
# a dictionary
data = json.load(f)
 
# Iterating through the json
# list
for i in data['NOSOTROS Policía Volador Bicicleta Robot Simulador']:
    print(i['likes'])
 
# Closing file
f.close()
"""