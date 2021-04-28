from flask import Flask
app = Flask(__name__)

@app.route('/query')
def query(className):
    # MATCH CLASSNAME WITH CODE IN ELASTICSEARCH HERE

    # RETURN RESULTS AS JSON
    return results

# Test function, try to display the time on the front end
@app.route('/time')
def get_current_time():
    return {'time': time.time()}

if __name__ == '__main__':
    app.run(port=2222)
