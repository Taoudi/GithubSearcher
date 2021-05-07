from flask import Flask
from flask import render_template
from flask import request
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

        x= '''{"hits" : [
            {
                "name" : "quicksort",
                "url" : "https://github.com/Taoudi/DD2476",
                "method_or_class" : "method",
                "codeblock" : "private static List<Number> quicksort (List<Number> list)"
            },
            {
                "name" : "slowsort",
                "url" : "https://github.com/Taoudi/DD2476",
                "method_or_class" : "method",
                "codeblock" : "private static List<Number> quicksort (List<Number> list)"
            }
            ]
        }'''

        output = json.loads(x)


        return render_template("example.html", output = json.dumps(output))

    else:
        return render_template("example.html")

# Test function, try to display the time on the front end
@app.route('/time')
def get_current_time():
    return {'time': time.time()}

if __name__ == '__main__':
    app.run(port=2222)
