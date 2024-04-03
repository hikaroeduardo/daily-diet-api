from flask import Flask, jsonify, request
from database import db
from models.models import User, Food
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import bcrypt

app = Flask(__name__)
login_manager = LoginManager()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "secret_key_test"

db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(id):
    return db.session.execute(db.select(User).filter_by(id=id)).scalar_one()

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
    
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({ "Message": "Logout realizado com sucesso!" })

@app.route('/foods', methods=['GET'])
@login_required
def foods():
    user = current_user

    foods = []

    for food in user.foods:
        serialized_food = {
            "id": food.id,
            "name": food.name,
            "description": food.description,
            "date": food.date
        }

        foods.append(serialized_food)

    return jsonify({ "foods": foods })

@app.route('/foods', methods=['POST'])
@login_required
def create_food():
    try:
        user = current_user

        data = request.json
        name = data["name"]
        description = data["description"]

        food = Food(name=name, description=description, user=user)

        db.session.add(food)
        db.session.commit()

        return jsonify({ "Message": f"{name} adicionado com sucesso!" })
    except:
        return jsonify({ "Message": "Não foi possível inserir o alimento, tente novamente. "})

if __name__ == "__main__":
    app.run(debug=True)