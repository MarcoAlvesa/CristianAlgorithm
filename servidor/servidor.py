import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/tempo', methods=['GET'])
def obter_tempo():
    tServer = time.time()
    T2 = time.time() 
    return jsonify({"tServer": tServer, "T2": T2})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)