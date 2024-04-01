from flask import Flask, jsonify, request
from database import db
from models.models import User, Food
from flask_login import LoginManager, login_user
import bcrypt

app = Flask(__name__)
login_manager = LoginManager()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "secret_key_test"

db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(id):
    return User.get(id)

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

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data["email"]
        password = data["password"]

        user = db.session.execute(db.select(User).filter_by(email=email)).scalar()

        if user and bcrypt.checkpw(str.encode(password), user.password):
            login_user(user)
            return jsonify({ "Message": "Login realizado com sucesso!" })
        
        return jsonify({ "Message": "Usuário não encontrado." }), 404
    except KeyError:
        return jsonify({ "Message": "Todos os campos são obrigatórios." }), 400

if __name__ == "__main__":
    app.run(debug=True)