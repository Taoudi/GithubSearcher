from flask import Flask
from flask import render_template
from flask import request
from engine import SearchEngine
import time
import os
import json

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def query():
    if request.method == 'POST':
    # MATCH CLASSNAME WITH CODE IN ELASTICSEARCH HERE
    # I harcoded an answer, now we should put the real hits json in the output

        query = request.form['query']
        
        eng = SearchEngine()
        x = dict()
        x['hits'] = eng.get_all_files()
        #with open("example.json",'w') as fp:
        #    fp.write(str(x))
        #x= "{'hits' : "+ str(eng.get_all_files()) + "}"
        #print(eng.get_all_files()[0])
        #print(x)
        output = json.loads(str(x))
        #print(output)
        #print(output)


        return render_template("interface.html", output = json.dumps(x))

    else:
        return render_template("interface.html")

# Test function, try to display the time on the front end
@app.route('/time')
def get_current_time():
    return {'time': time.time()}

if __name__ == '__main__':
    app.run(port=2222)
