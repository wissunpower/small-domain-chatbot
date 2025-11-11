
import time

from multiprocessing.managers import BaseManager
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# initialize manager connection
# NOTE: you might want to handle the password in a less hardcoded way
manager = BaseManager(('localhost', 5602), b'password')
manager.register('query_index')


@app.route("/query", methods=["GET"])
def query_index():
    global manager
    query_text = request.args.get("text", None)
    if query_text is None:
        return "No text found, please include a ?text=blah parameter in the URL", 400
    
    response = manager.query_index(query_text)._getvalue()
    response_json = {
        "text": str(response),
        "sources": [{"text": str(x.text), 
                     "similarity": round(x.score, 2),
                     "doc_id": str(x.id_),
                     "start": x.node.node_info['start'],
                     "end": x.node.node_info['end'],
                    } for x in response.source_nodes]
    }
    return make_response(jsonify(response_json)), 200

@app.route("/")
def home():
    return "Hello, World! Welcome to the small domain chatbot!"


def run_handler():
    time.sleep(10)
    
    manager.connect()

    app.run(host="0.0.0.0", port=5601)

if __name__ == "__main__":
    run_handler()
