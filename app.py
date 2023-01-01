from flask import Flask, request

app = Flask(__name__)

# xxx
@app.route('/api/x', methods=['GET'])
def default():

    return {
        'status': 'ok'
    }