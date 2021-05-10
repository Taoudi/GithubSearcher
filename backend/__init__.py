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
    
        # 2 parameters for elasticsearch : query and Search by

        # Query : content of the query
        query = request.form['query']
        # Search by : 3 possible values: "name", "methods", "name_and_methods"
        search_by = request.form['search_by']
        
        eng = SearchEngine()
        x = dict()
        x['hits'] = eng.get_all_files()
        #with open("example.json",'w') as fp:
        #    fp.write(str(x))
        #output = json.loads(str(x))
        output = json.dumps(x)
        output = output.replace('\\', '\\\\')


        return render_template("interface.html", output = output)

    else:
        return render_template("interface.html")

# Test function, try to display the time on the front end
@app.route('/time')
def get_current_time():
    return {'time': time.time()}

if __name__ == '__main__':
    app.run(port=2222)
