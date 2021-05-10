import json
import time

from flask import Flask
from flask import render_template
from flask import request

from engine import SearchEngine

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

        field = search_by
        name = query.lower()
        print(name, field)
        if field == "name_and_methods":
            x['hits'] = eng.search_OR(name)
        else:
            x['hits'] = eng.search(name, field)
        output = json.dumps(x)
        output = output.replace('\\', '\\\\')

        return render_template("interface.html", output=output)

    else:
        return render_template("interface.html")


# Test function, try to display the time on the front end
@app.route('/time')
def get_current_time():
    return {'time': time.time()}


if __name__ == '__main__':
    app.run(port=2222)
