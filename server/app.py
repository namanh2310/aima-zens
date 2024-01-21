from flask import Flask
from flask_cors import CORS
from routes.Router import Router

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/", methods=["GET"])
def index():
    return 'Restful API Successfully Called!!!'

Router.run(app)

if __name__ == '__main__':
    app.run(host='localhost', port='8081', debug=True)


