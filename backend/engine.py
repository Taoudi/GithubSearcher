from elasticsearch import Elasticsearch, helpers


class SearchEngine:
    def __init__(self):
        self.es = Elasticsearch()

    def get_all_files(self):
        res = self.es.search(
            index="javafiles",
            size=1000,
            request_timeout=1000  # type error!
        )
      
        return [j['_source'] for j in res['hits']['hits']][0:10]
