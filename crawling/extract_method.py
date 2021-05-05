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
    class_name = re.findall('(public|private) class (\w*)', code)

    
    p = re.compile('(public|private|protected)\\s+(static\\s+)*([A-Za-z\\<\\>]+)\\s+(\\w+)\\s*\\(\\s*(\\w+\\s+\\w+)*((\\s*,\\s*\\w+\\s+\\w+)*)\\s*\\)')# p - w - - w
    #p = re.compile('(\\w+)(\\()(\\w+)(,\\s*\\w+)*(\\))')
    s = re.findall(p,code,flags=0)
    for func in s:
        print(func)
    #tokens = nltk.word_tokenize(s)
    print("------------------------")
    return s,class_name

##Pulling the urls from url file
with open("javaurls",'r') as fp:
    for url in fp:
        urls.append(url)

urls= ["https://raw.githubusercontent.com/Taoudi/FairGrounds/master/src/main/java/FairGrounds/Application/ApplicationSearchService.java","https://raw.githubusercontent.com/Taoudi/FairGrounds/master/src/main/java/FairGrounds/Presentation/ApplicationExpertiseFormValidator.java"]
for url in urls:
    try:
        # response = http.urlopen('GET',url)
        response = urllib.request.urlopen(url)
        code = response.read().decode("utf-8")
        codes.append(code)
        tokens, name = pre_process(code)
        clean_code.append(tokens)
        class_names.append(name)
        clean_url = url.split(".com/")[1]
        part_url = clean_url.split("/")
        username = part_url[0]
        repo = part_url[1]
        javafilename = part_url[len(part_url)-1].replace(".java","")
        print(url)
        #print("java_files/"+username+"_"+repo+"_"+javafilename.replace("\n",""))
        #print(username+"_"+repo+"_"+javafilename)
        #print(name)
        #for i, name in enumerate(name):
        #    with open("java_files/"+username+"_"+repo+"_"+javafilename.replace("\n",""),'w') as fp:
        #        fp.write(tokens)
        #        pass
    except urllib.error.HTTPError:
        continue
        

for i,code in enumerate(clean_code):
    if "main" in code:
        index['code'].append(codes[i])
        index['name'].append(class_names[i])
        print(index['name'])
        #with open(index['name'][i],'w') as fp:
        #    fp.write(index['code'][i])

