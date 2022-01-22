from flask import Flask, request, jsonify
from flask_cors import CORS
from youtubedl import *
from objects.Source import Source
from methods_controller import *

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return "BilyGine Downloader Index Page"
    
@app.route('/api/download', methods=['POST', 'PUT', 'DELETE'])
def downloader():
    if request.method == 'POST':
        url = request.args.get('url')
        return jsonify(create_new_source(url))
    elif request.method == 'PUT':
        return "not implemented yet"
    elif request.method == 'DELETE':
        source_id = request.args.get('source_id')
        return jsonify(delete_source(source_id))
    else:
        return "ko"

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
