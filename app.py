from flask import Flask, request, jsonify
from flask_cors import CORS
from ai_engine import generate

app = Flask(__name__)
CORS(app)

@app.route("/api/relations", methods=["POST"])
def relations():
    data = request.json
    response = generate(data)

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555)

