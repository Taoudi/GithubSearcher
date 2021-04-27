from flask import jsonify

import urllib.request
import nltk
import re
import ssl

# # http = urllib3.PoolManager()
codes = []
urls = []
programs = []
clean_code = []
class_names = []
index = {'code': [],'name':[]}


def pre_process(code):
    class_name = re.findall('class (\w*)', code)
    s = re.sub('[^a-zA-Z0-9]', ' ', code)
    tokens = nltk.word_tokenize(s)
    return tokens,class_name

##Pulling the urls from url file
with open("/Users/nandakishorprabhu/Documents/Studies/DD2476/Github Search/DD2476/crawling/javaurls",'r') as fp:
    for url in fp:
        urls.append(url)

for url in urls:
    # response = http.urlopen('GET',url)
    response = urllib.request.urlopen(url)
    code = response.read().decode("utf-8")
    codes.append(code)
    tokens, name = pre_process(code)
    clean_code.append(tokens)
    class_names.append(name)

for i,code in enumerate(clean_code):
    if "main" in code:
        index['code'].append(codes[i])
        index['name'].append(class_names[i])

print(index)