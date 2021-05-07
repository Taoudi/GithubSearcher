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

class Code:
    def __init__(self,functions, codeblock, url):
        self.codeblock = codeblock
        self.functions = functions
        self.url = url

    def jsonify(self):
        string =  "{ url:" + self.url + ",\nfunctions:" + "["
        for i,f in enumerate(self.functions):
            string+=f.jsonify()
            if i< len(self.functions)-1:
                string+=", "
        
        string+="]" +  ",\ncodeblock:{\n"+self.codeblock + "\n}\n}"
        return string

class Parameter:
    def __init__(self,name, v_type):
        self.name = name
        self.type = v_type
    
    def jsonify(self):
        return "{ 'name':" + self.name + ",'type" +self.type + "}"
    def __str__(self):
        return self.name + " " + self.type

class Method:
    def __init__(self,access_modifier="", static=False,return_type="",method_name="",parameters=list()):
        self.access_modifier = access_modifier
        self.static = static
        self.return_type = return_type
        self.method_name = method_name
        self.parameters = parameters

    def __str__(self):
        string = self.access_modifier
        if self.static:
            string+=" " + "static"
        string+=" " + self.return_type + " " + self.method_name + "("
        if len(self.parameters) == 0:
            return string+")"
        elif len(self.parameters) == 1:
            return string+str(self.parameters[0])+")"
        else:
            for i,p in enumerate(self.parameters):
                string+=str(p)
                if i < len(self.parameters)-1:
                    string+=", "
            return string+")"


    def jsonify(self):
        string = "{ access_modifier:" +self.access_modifier+ ", " 
        if self.static:
            string+="static: " + "True, "
        else:
            "static: " + "False, "

        string+="return_type:" + self.return_type + ", method_name:" + self.method_name + ", "
        if len(self.parameters) == 0:
            return string+"parameters:[] }"
        elif len(self.parameters) == 1:
            return string+"parameters:["+"{ type:" +self.parameters[0].type +", name:" +self.parameters[0].name+"}"+ "] }"
        else:
            string+="parameters:["
            for i,p in enumerate(self.parameters):
                string+="{ type:" +p.type +", name:" +p.name+"}"
                if i < len(self.parameters)-1:
                    string+=", "
            return string+"] }"



def pre_process(code):
    class_name = re.findall('(public|private) class (\w*)', code)
    invalid_fields = ["new", "private", "public","protected"]
    
    p = re.compile('(public|private|protected)?\\s+(static\\s+)?([A-Za-z\\<\\>\\[\\]]+)\\s+(\\w+)\\s*\\(\\s*((\\s*,*\\s*[\\w\\[\\]\\<\\>]+\\s+\\w+,*)*)\\)')# p - w - - w
    #p = re.compile('(public|private|protected)?\\s+(static)?\\s+([A-Za-z\<\\>\\[\\]]+)\\s+(\\w+)\\s*\\(\\s*(\\s*,*\\s*[\\w\\[\\]]+\\s+\\w+,*)*\\)')
    #p = re.compile('(\\w+)(\\()(\\w+)(,\\s*\\w+)*(\\))')
    s = re.findall(p,code,flags=0)
    methods= list()
    for func in s:
        access_modifier = ""
        static = False
        return_type = ""
        method_name = ""
        parameters = list()
        invalid = False
        for i,f in enumerate(func):
            if i == 0:
                access_modifier = re.sub(r"\s+", '', f)
            elif i==1:
                if f!="":
                    static=True
            elif i ==2:
                return_type = re.sub(r"\s+", '', f)
                #print(return_type)
                if return_type in invalid_fields:
                    invalid = True
                    break
            elif i ==3:
                method_name = re.sub(r"\s+", '', f)
            elif i==4:
                parameters = []
                parameter_sets = f.split(",")
                for pars in parameter_sets:
                    if len(pars)>1:
                        parameters.append(Parameter(v_type=pars.split()[0],name=pars.split()[1]))
        #print(func)
        if not invalid:
            meth = Method(access_modifier=access_modifier,static=static,return_type=return_type,method_name=method_name,parameters=parameters)
            methods.append(meth)
            print(meth)
            print(func)

        #print(meth)
        #print(str(meth))
    #tokens = nltk.word_tokenize(s)
    print("------------------------")
    return methods

##Pulling the urls from url file
with open("javaurls",'r') as fp:
    for url in fp:
        urls.append(url)

#urls= ["https://raw.githubusercontent.com/Taoudi/FairGrounds/master/src/main/java/FairGrounds/Application/ApplicationSearchService.java","https://raw.githubusercontent.com/Taoudi/FairGrounds/master/src/main/java/FairGrounds/Presentation/ApplicationExpertiseFormValidator.java"]
for url in urls:
    try:
        # response = http.urlopen('GET',url)
        print(url)
        response = urllib.request.urlopen(url)
        code = response.read().decode("utf-8")
        methods = pre_process(code)
        clean_url = url.split(".com/")[1]
        part_url = clean_url.split("/")
        username = part_url[0]
        repo = part_url[1]
        javafilename = part_url[len(part_url)-1].replace(".java","")

        c = Code(methods,code,url)
        #print("java_files/"+username+"_"+repo+"_"+javafilename.replace("\n",""))
        #print(username+"_"+repo+"_"+javafilename)
        #print(name)
        #for i, name in enumerate(name):
        with open("java_files/"+username+"_"+repo+"_"+javafilename.replace("\n",""),'w') as fp:
            fp.write(c.jsonify())
    except urllib.error.HTTPError:
        continue

