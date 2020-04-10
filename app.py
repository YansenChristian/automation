from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/', methods=['GET'])
def respond():
    name = request.args.get("name", None)
    name = name if name is not None else "Guest"
    return name

if __name__ == '__main__':
    app.run(threaded=True, port=8000)