from config import Config
from app.models import User
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, flash, render_template, request
from app import db
from app.forms import LoginForm
from flask_login import login_user
app = Flask(__name__)
app.config.from_object(Config)

#db = SQLAlchemy(app)
#app.config['SQLALCHEMY_DATABASE_URI']
#db.init_app(app)
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title="Home Page")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Проверяем, есть ли пользователь в базе данных
        user = User.query.filter_by(email=email).first()
        # Если пользователя нет или пароль неверный, выведите сообщение об ошибке
        if user is None:
            return 'Неверный email'
        elif not user.check_password(password):
            return 'Неверный пароль'
        else:
            return 'Вход успешно выполнен'
    return render_template('loginform.html')




@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # Получить данные из формы
        fullname = request.form['fullname']
        email = request.form['name']
        password = request.form['password']

        # Создать нового пользователя
        new_user = User(username=fullname, email=email)
        new_user.set_password(password)

        # Добавить пользователя в базу данных
        db.session.add(new_user)
        db.session.commit()

        return 'Регистрация успешно завершена.'

    # Отобразить форму регистрации
    return render_template('registerform.html')

@app.route('/normative')
def normative():
    return render_template('formnormative.html')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
