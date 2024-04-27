from config import Config
from app.models import User, Student
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, flash, render_template, request
from app import db
import re

app = Flask(__name__)
app.config.from_object(Config)


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
        fullname = request.form['fullname']
        email = request.form['name']
        password = request.form['password']
        # Проверить соответствие email реальному формату
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            return 'Неверный формат email.'
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return 'Пользователь с таким email уже существует.'  # спросить у Даши:
            # можно ли просто всплывающим сообщением проверять сообщать об этом
        new_user = User(username=fullname, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return 'Регистрация успешно завершена.'
    return render_template('registerform.html')


@app.route('/normative', methods=['GET', 'POST'])
def normative():
    if request.method == 'POST':
        name = request.form.get('Имя')
        course = request.form.get('Курс')
        group = request.form.get('Группа')
        gender = request.form.get('Пол')
        jump = request.form.get('Прыжок')
        rise = request.form.get('Подъем')
        slant = request.form.get('Наклон')
        pullup = request.form.get('Подтягивание')
        mark = request.form.get('Оценка')
        new_student = Student(name=name, course=course, group=group, gender=gender, jump=jump, rise=rise, slant=slant, pullup=pullup, mark=mark)
        db.session.add(new_student)
        db.session.commit()
        return render_template('formnormative.html', message='Студент добавлен в базу')
    else:
        return render_template('formnormative.html')

@app.route('/table')
def table_view():
    student = Student.query.order_by(Student.name).all()
    return render_template('table.html', student=student)

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
