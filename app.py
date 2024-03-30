from flask import Flask, jsonify
from database import db
from models.models import User, Food

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify({ "Message": "Hello World" })

if __name__ == "__main__":
    app.run(debug=True)