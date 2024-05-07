from config import Config
from app.models import User, Student
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, flash, render_template, request, session
from app import db
import re
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id # Пользователь аутентифицирован, устанавливаем сессию
            return redirect(url_for('table_view'))
        else:
            flash('Неверный email или пароль')
            return redirect(url_for('login'))
    return render_template('loginform.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['name']
        password = request.form['password']
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            return 'Неверный формат email.'
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return 'Пользователь с таким email уже существует.'
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
        new_student = Student(name=name, course=course, group=group, gender=gender, jump=jump, rise=rise, slant=slant,
                              pullup=pullup, mark=mark)
        db.session.add(new_student)
        db.session.commit()
        return render_template('formnormative.html', message='Студент добавлен в базу')
    else:
        return render_template('formnormative.html')

@app.route('/table')
def table_view():
    if 'user_id' in session:
        students = Student.query.order_by(Student.name).all()
        return render_template('table.html', students=students)
    else:
        return redirect(url_for('login'))

@app.route('/table/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get(id)
    if not student:
        return "Студент не найден", 404
    if request.method == 'POST':
        student.name = request.form.get('Имя')
        student.course = request.form.get('Курс')
        student.group = request.form.get('Группа')
        student.gender = request.form.get('Пол')
        student.jump = request.form.get('Прыжок')
        student.rise = request.form.get('Подъем')
        student.slant = request.form.get('Наклон')
        student.pullup = request.form.get('Подтягивание')
        student.mark = request.form.get('Оценка')
        try:
            db.session.commit()
            return redirect(url_for('table_view'))
        except Exception as e:
            db.session.rollback()  # Откат изменений в случае ошибки
            return f"Возникла ошибка: {e}", 500
    return render_template('formnormative_edit.html', student=student)

@app.route('/table/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    try:
        db.session.delete(student)
        db.session.commit()
        return redirect('/table')
    except:
        return "При удалении студента возникла ошибка"


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
