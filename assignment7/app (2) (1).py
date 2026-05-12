# =============================================================================
# A7: Full-Text Search - Flask API
# =============================================================================
# SETUP (run these before starting the app):
#
# 1. Start ElasticSearch (keep this terminal open):
#    cd ~/elasticsearch-8.13.0
#    export ES_JAVA_OPTS="-Xms512m -Xmx512m"
#    bin/elasticsearch -d -p pid
#
# 2. Run the notebooks in order:
#    - a7_skeleton.ipynb    → parses XML, indexes 'pubmed' with nltk preprocessing
#    - a7_extension.ipynb  → indexes 'pubmed_ext' with ES built-in analyzer
#
# 3. Start the Flask app:
#    cd ~/databases_public_policy/assignment7
#    .venv/bin/python app.py
#
# 4. Open Swagger UI at: http://127.0.0.1:5000/apidocs/
#
# ENDPOINTS:
#   GET /keyword_search?keyword=cancer
#   GET /count_docs?required=cancer&exclude=lung
#   GET /keyword_search_with_typo?keyword=canser&fuzziness=AUTO
#
# INDEXES:
#   pubmed     → nltk preprocessed (stopwords removed + lemmatized)
#   pubmed_ext → ES analyzer (stopwords + stemming via pubmed_analyzer)
# =============================================================================

from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Connect to local ElasticSearch instance
es = Elasticsearch('http://localhost:9200')

# Index names
INDEX_NAME = 'pubmed'      # Part 1 & 2: nltk-preprocessed index
EXT_INDEX  = 'pubmed_ext'  # Part 3 Extension: ES-analyzer index


# ---------------------------------------------------------------------------
# Part 2 — Endpoint 1: Simple keyword search (exact match)
# ---------------------------------------------------------------------------
@app.route('/keyword_search', methods=['GET'])
def keyword_search():
    """
    Search abstracts by keyword (exact match).
    ---
    parameters:
      - name: keyword
        in: query
        type: string
        required: true
        description: The keyword to search for in abstracts.
    responses:
      200:
        description: A list of matching documents.
      400:
        description: Missing keyword parameter.
    """
    keyword = request.args.get('keyword', '').strip().lower()

    if not keyword:
        return jsonify({'error': 'Please provide a keyword parameter.'}), 400

    query = {
        'query': {
            'match': {
                'abstract': {
                    'query': keyword,
                    'operator': 'and'
                }
            }
        },
        'size': 100
    }

    response = es.search(index=INDEX_NAME, body=query)
    hits = response['hits']['hits']

    results = [
        {
            'pmid':     hit['_source']['pmid'],
            'title':    hit['_source']['title'],
            'abstract': hit['_source']['abstract'],
            'score':    hit['_score']
        }
        for hit in hits
    ]

    return jsonify({
        'keyword':       keyword,
        'total_results': len(results),
        'results':       results
    })


# ---------------------------------------------------------------------------
# Part 2 — Endpoint 2: Count docs with required keyword, optionally excluding
#           abstracts that contain another keyword.
# ---------------------------------------------------------------------------
@app.route('/count_docs', methods=['GET'])
def count_docs():
    """
    Count abstracts containing a required keyword, optionally excluding another.
    ---
    parameters:
      - name: required
        in: query
        type: string
        required: true
        description: Keyword that MUST appear in the abstract.
      - name: exclude
        in: query
        type: string
        required: false
        description: Keyword that must NOT appear in the abstract (optional).
    responses:
      200:
        description: Count of matching documents.
      400:
        description: Missing required keyword parameter.
    """
    required = request.args.get('required', '').strip().lower()
    exclude  = request.args.get('exclude',  '').strip().lower()

    if not required:
        return jsonify({'error': 'Please provide a required keyword parameter.'}), 400

    must_clause     = [{'match': {'abstract': required}}]
    must_not_clause = [{'match': {'abstract': exclude}}] if exclude else []

    query = {
        'query': {
            'bool': {
                'must':     must_clause,
                'must_not': must_not_clause
            }
        }
    }

    response = es.count(index=INDEX_NAME, body=query)
    count = response['count']

    return jsonify({
        'required': required,
        'exclude':  exclude if exclude else None,
        'count':    count
    })


# ---------------------------------------------------------------------------
# Part 3 Extension — Endpoint 3: Keyword search with typo tolerance (fuzzy)
# ---------------------------------------------------------------------------
@app.route('/keyword_search_with_typo', methods=['GET'])
def keyword_search_with_typo():
    """
    Search abstracts by keyword with typo tolerance (fuzzy matching).
    ---
    parameters:
      - name: keyword
        in: query
        type: string
        required: true
        description: The keyword to search for (typos allowed, e.g. 'canser' matches 'cancer').
      - name: fuzziness
        in: query
        type: string
        required: false
        default: AUTO
        description: Edit distance for fuzzy matching. One of AUTO, 0, 1, 2 (default AUTO).
    responses:
      200:
        description: A list of matching documents.
      400:
        description: Missing keyword parameter.
    """
    keyword   = request.args.get('keyword',   '').strip().lower()
    fuzziness = request.args.get('fuzziness', 'AUTO').strip().upper()

    if not keyword:
        return jsonify({'error': 'Please provide a keyword parameter.'}), 400

    if fuzziness not in {'AUTO', '0', '1', '2'}:
        fuzziness = 'AUTO'

    query = {
        'query': {
            'match': {
                'abstract': {
                    'query':     keyword,
                    'fuzziness': fuzziness,
                    'operator':  'and'
                }
            }
        },
        'size': 100
    }

    response = es.search(index=EXT_INDEX, body=query)
    hits = response['hits']['hits']

    results = [
        {
            'pmid':     hit['_source']['pmid'],
            'title':    hit['_source']['title'],
            'abstract': hit['_source']['abstract'],
            'score':    hit['_score']
        }
        for hit in hits
    ]

    return jsonify({
        'keyword':       keyword,
        'fuzziness':     fuzziness,
        'total_results': len(results),
        'results':       results
    })


if __name__ == '__main__':
    app.run(debug=True)