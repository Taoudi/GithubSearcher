from elasticsearch import Elasticsearch


class SearchEngine:
    def __init__(self):
        self.es = Elasticsearch()

    def get_all_files(self):
        res = self.es.search(
            index="javafiles",
            size=1000,
            request_timeout=1000
        )
        return [j['_source'] for j in res['hits']['hits']][0:10]

    def search_OR(self, name=''):
        res = self.es.search(index="javafiles", size=100, body={"query": {
            "bool": {
                "should": [
                    {"match": {"name": name}},
                    {"match": {"methods": name}}
                ],
            }
        }
        })
        print(len(res['hits']['hits']))
        for i in res['hits']['hits']:
            del i['_source']['codeblock']
        return [j['_source'] for j in res['hits']['hits']]

    def search(self, name, field):
        res = self.es.search(index="javafiles", size=100, body={
            "query": {"match": {str(field): name}}
        })
        print(len(res['hits']['hits']))
        for i in res['hits']['hits']:
            del i['_source']['codeblock']

        return [j['_source'] for j in res['hits']['hits']]
