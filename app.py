from flask import Flask, jsonify, request
from database import db
from models.models import User, Food
import bcrypt

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)

@app.route('/register', methods=['POST'])
def create_user():
    try:
        data = request.json
        
        name = data["name"]
        email= data["email"]
        password = data["password"]

        user = User(name=name, email=email, password=bcrypt.hashpw(str.encode(password), bcrypt.gensalt()))

        db.session.add(user)
        db.session.commit()

        return jsonify({ "Message": "Usuário cadastrado com sucesso!" })
    except KeyError:
        return jsonify({ "Message": "Todos os campos são obrigatórios." }), 400

if __name__ == "__main__":
    app.run(debug=True)