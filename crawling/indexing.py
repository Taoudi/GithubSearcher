from elasticsearch import Elasticsearch, helpers
import urllib.request
import re
import ssl
from extract_method import Code, Method, Parameter
class Indexer:
    def pre_process(self,code):
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
                methods.append(str(meth))
        return methods


    def get_urls(self,filename="javaurls"):
        ##Pulling the urls from url file
        urls=[]
        with open(filename,'r') as fp:
            for url in fp:
                urls.append(url)
        return urls

    def fetch_data(self):
        urls = self.get_urls()
        data = []
        for index,url in enumerate(urls):
            try:
                # response = http.urlopen('GET',url)
                #print(url)
                response = urllib.request.urlopen(url)
                code = response.read().decode("utf-8")
                methods = self.pre_process(code)
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
                #d = dict()
                jsoned = {
                        'codeblock':c.codeblock,
                        'url':c.url,
                        'method_or_class':'class',
                        'name':javafilename,
                        'methods':methods
                    }
                #d['codeblock'] = c.codeblock
                #d['url'] = c.url
                #d['method_or_class'] = "class"
                #d['name'] = javafilename
                #d['_index'] = jsoned
                #d['_id'] = index
                #with open("java_files/"+username+"_"+repo+"_"+javafilename.replace("\n",""),'w') as fp:
                    #fp.write(c.jsonify())
                #    fp.write(str(d))
                data.append(jsoned)
            except urllib.error.HTTPError:
                continue
        return data


    def index(self,data):
        es = Elasticsearch()


        for i,node in enumerate(data):
            es.index(index='javafiles',id=i,body=node)
        #helpers.bulk(es,data)





if __name__ == "__main__":
    i = Indexer()
    data = i.fetch_data()  
    print(len(data), "files parsed")
    i.index(data)

    es = Elasticsearch()
    res = es.search(
        index="javafiles",
        size=1000,
        request_timeout=1000  # type error!
    )
    print("Got ",res['hits']['total']['value'], "hits")
    real_res = [ j['_source'] for j in  res['hits']['hits']]
    for i in real_res:
        print(i)
        break
