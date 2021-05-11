## DD2476 - GithubSearcher

### Group Members
E-Joon Ko, Youssef Taoudi, Nandakishor Prabhu Ramlal, Emile Lucas

### Indexing

Extract the data.zip file as data

Run the indexing.bat file (After setting up elasticsearch, see below)



### Run Backend

In the project directory, run:

`export FLASK_APP=backend`

`flask run`

In Windows, use instead:

`set FLASK_APP=backend`

`flask run`

Then open http://127.0.0.1:5000/ on your navigator.

Modules that need to be pip installed:
- flask

Alternatively run the start_server.bat file which starts the server through python.

### ElasticSearch
For running ElasticSearch and Kibana, make sure to have OPENJDK for the Java runtime environment (AdoptOpenJDK11 was used for this project.)

#### Setting up ElasticSearch
For setting up the ElasticSearch server, the simplest method is to download the compressed folder at: 
https://www.elastic.co/downloads/elasticsearch. Once downloaded, the ElasticSearch server can be started by running the executable file
in bin (elasticsearch.bat in Windows). The ElasticSearch server is default located at http://localhost:9200/.

#### Setting up Kibana
For setting up a Kibana server to act as an interface for the ElasticSearch server, download the compressed
folder at: https://www.elastic.co/downloads/kibana. Once downloaded, the Kibana server can be started by running the executable file
in bin (kibana.bat in Windows). The Kibana server is default located at http://localhost:5601/.

Setting up the Index for ElasticSearch in Kibana
```
DELETE javafiles

PUT javafiles
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_custom_analyzer": {
          "type": "custom", 
          "tokenizer": {
              "custom_tokenizer": {
                  "type": "ngram",
                      "min_gram": 2,
                      "max_gram": 30,
                      "token_chars": [
                          "letter",
                          "digit",
                          "symbol",
                          "punctuation"
                        ]
               }
          },
          "char_filter": [
            "html_strip"
          ],
          "filter": [
            "lowercase",
            "asciifolding"
          ]
        }
      }
    }
  }
  ```

#### Indexing with ElasticSearch
Every object indexed into the ElasticSearch Server will be a JSON Object with the following variables:
```
  "name": "class/function name",
  "url": "website url",
  "methods": "list of methods"
```

Indexing via the interface was done through using the match API and put API:
```
PUT /<_index>/<_type>/<docID>
{
  "name": "class/function name",
  "url": "website url",
  "methods": "list of methods"
}
```

#### Searching with ElasticSearch
Searching via the interface was done using the search API and bool API for filtering the search topic:

```
POST file/_search
{
  "query": {
    "bool" : {
      "should": [
        {"match":{"name":"name"}},
        {"match":{"methods": "method name"}}
      ]
    }
  }
}
```

#### Using ElasticSearch on the Python Interface
```
from elasticsearch import Elasticsearch
es = Elasticsearch()
es.search(index="test-index", body={put query here})
```
