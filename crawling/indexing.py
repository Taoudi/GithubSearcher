import re
import urllib.request
import time
import os

from elasticsearch import Elasticsearch

from extract_method import Code, Method, Parameter


class Indexer:
    def pre_process(self, code):
        class_name = re.findall('(public|private) class (\w*)', code)
        invalid_fields = ["new", "private", "public", "protected"]

        p = re.compile(
            '(public|private|protected)?\\s+(static\\s+)?([A-Za-z\\<\\>\\[\\]]+)\\s+(\\w+)\\s*\\(\\s*((\\s*,*\\s*[\\w\\[\\]\\<\\>]+\\s+\\w+,*)*)\\)')  # p - w - - w
        # p = re.compile('(public|private|protected)?\\s+(static)?\\s+([A-Za-z\<\\>\\[\\]]+)\\s+(\\w+)\\s*\\(\\s*(\\s*,*\\s*[\\w\\[\\]]+\\s+\\w+,*)*\\)')
        # p = re.compile('(\\w+)(\\()(\\w+)(,\\s*\\w+)*(\\))')
        s = re.findall(p, code, flags=0)
        methods = list()
        for func in s:
            access_modifier = ""
            static = False
            return_type = ""
            method_name = ""
            parameters = list()
            invalid = False
            for i, f in enumerate(func):
                if i == 0:
                    access_modifier = re.sub(r"\s+", '', f)
                elif i == 1:
                    if f != "":
                        static = True
                elif i == 2:
                    return_type = re.sub(r"\s+", '', f)
                    # print(return_type)
                    if return_type in invalid_fields:
                        invalid = True
                        break
                elif i == 3:
                    method_name = re.sub(r"\s+", '', f)
                elif i == 4:
                    parameters = []
                    parameter_sets = f.split(",")
                    for pars in parameter_sets:
                        if len(pars) > 1:
                            parameters.append(Parameter(v_type=pars.split()[1], name=pars.split()[0]))
            # print(func)
            if not invalid:
                meth = Method(access_modifier=access_modifier, static=static, return_type=return_type,
                              method_name=method_name, parameters=parameters)
                methods.append(str(meth))
                #print(str(meth))
        #print("-----------------------------")
        return methods

    def get_urls(self, filename="javaurls2"):
        ##Pulling the urls from url file
        urls = []
        with open(filename, 'r') as fp:
            for url in fp:
                urls.append(url)
        return urls

    def fetch_data(self, max_iters=1000000):
        #urls = self.get_urls()
        data = []
        directory = "data"
        #print(len(os.listdir(directory)))
        for index,filename in enumerate(os.listdir(directory)):
            try:
               
                # response = http.urlopen('GET',url)
                # print(url)
                """response = urllib.request.urlopen(url)
                code = response.read().decode("utf-8")
                
                clean_url = url.split(".com/")[1]
                part_url = clean_url.split("/")
                username = part_url[0]
                repo = part_url[1]
                javafilename = part_url[len(part_url) - 1].replace(".java", "")"""
                temp = os.path.join(directory, filename)
                f = open(os.path.join(directory, filename),'r')
                #print(f.read())
                
                temp = f.read().split('\n',1)
                url = temp[0]
                if index%100==0:
                    print(index)
                if index >2000:
                    #print(url)
                    #print(temp[1])
                    #print("------------------------------------------")
                    pass
                clean_url = url.split(".com/")[1]
                part_url = clean_url.split("/")
                javafilename = part_url[len(part_url) - 1].replace(".java", "")
                code = temp[1]#.decode("utf-8")
                #print(url)
                #print("yo")
                methods = self.pre_process(code)
                #print("yo2")
                c = Code(methods, code, url)
                jsoned = {
                    'url': c.url,
                    'method_or_class': 'class',
                    'name': javafilename,
                    'methods':methods
                }
                data.append(jsoned)
                if index >= max_iters:
                    break
            except urllib.error.HTTPError:
                continue
            except UnicodeDecodeError:
                continue
        return data

    def index(self, data,max_iters=1000000):
        es = Elasticsearch()

        for i, node in enumerate(data):
            es.index(index='javafiles', id=i, body=node)
            if i == max_iters:
                break
        # helpers.bulk(es,data)


if __name__ == "__main__":
    iters = 100000
    start_time = time.time()
    i = Indexer()
    data = i.fetch_data(max_iters=iters)
    print(len(data), "files parsed")
    i.index(data,max_iters=iters)
    print("--- %s seconds ---" % (time.time() - start_time))


    es = Elasticsearch()
    res = es.search(
        index="javafiles",
        size=1000,
        request_timeout=1000  # type error!
    )
    print("Got ", res['hits']['total']['value'], "hits")
    """real_res = [j['_source'] for j in res['hits']['hits']]
    for i in real_res:
        print(i)
        break"""
