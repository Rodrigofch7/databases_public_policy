from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)

@app.route("/keyword_search", methods=["GET"])
def keyword_search():
    ...

@app.route("/keyword_search_with_typo", methods=["GET"])
def keyword_search_with_typo():
    ...

@app.route("/count_docs", methods=["GET"])
def count_docs():
    ...


if __name__ == "__main__":
    app.run(debug=True)