from config import Config, sign_in_key
from app.models import User, Student
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, flash, render_template, request, session, get_flashed_messages, send_file, make_response
from app import db
import re
from werkzeug.security import check_password_hash
import pandas as pd
from datetime import timedelta

app = Flask(__name__)
app.config.from_object(Config)
app.permanent_session_lifetime = timedelta(minutes=60)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id # Пользователь аутентифицирован, устанавливаем сессию
            session.permanent = True  # Устанавливаем сессию как постоянную, чтобы использовать permanent_session_lifetime
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
        email = request.form['email']
        password = request.form['password']
        registration_key = request.form['key']
        if registration_key != sign_in_key:
            flash('Неверный идентифицирующий код.')  # Использование flash для сообщения
            return render_template('registerform.html')
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            flash('Неверный формат email.')  # Использование flash для сообщения
            return render_template('registerform.html')
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Пользователь с таким email уже существует.')  # Использование flash для сообщения
            return render_template('registerform.html')
        try:
            new_user = User(username=fullname, email=email)
            new_user.set_password(password)  # Убедитесь, что этот метод корректно хэширует пароль
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            flash('Произошла ошибка при регистрации. Пожалуйста, попробуйте снова.')  # Использование flash для сообщения
            return render_template('registerform.html')
        return redirect(url_for('login'))  # После регистрации перенаправляем на страницу входа
    return render_template('registerform.html')

# !!!обработка 2 и 3 слов
def validate_name(name):
    if name is None:
        return False
    # Изменённое регулярное выражение, которое принимает два или три слова
    pattern = r"^[A-Za-zА-Яа-я]{2,20}(?:\s[A-Za-zА-Яа-я]{2,20}){1,2}$"
    return re.match(pattern, name) is not None

@app.route('/')
@app.route('/normative', methods=['GET', 'POST'])
def normative():
    response = make_response(render_template('formnormative.html'))
    if request.method == 'POST':
        # устанавливаем куки для отслеживания времени
        if request.cookies.get('has_submitted'):
            return make_response(render_template('formnormative.html', message='Вы уже отправили данные.'), 429)
        name = request.form.get('ФИО')
        if not validate_name(name):
            return render_template('formnormative.html', message='Некорректное имя и фамилия.')

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

        # Установить cookie, указывающий, что форма уже отправлена
        response.set_cookie('has_submitted', 'true', max_age=60*60*24)  # 24 часа
        response.data = render_template('formnormative.html', message='Студент добавлен в базу')
        return response
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


@app.route('/export')
def export(filename='students.xlsx'):
    students_query = db.session.query(Student).all()
    students_data = [
        {
            'ID': student.id,
            'ФИО': student.name,
            'Курс': student.course,
            'Группа': student.group,
            'Пол': student.gender,
            'Прыжок': student.jump,
            'Подъем': student.rise,
            'Растяжка': student.slant,
            'Подтягивания': student.pullup,
            'Оценка': student.mark
        } for student in students_query
    ]
    # Создание DataFrame из списка словарей
    df_students = pd.DataFrame(students_data)
    df_students.to_excel(filename, index=False)
    return send_file(filename, as_attachment=True)

@app.route('/change_pswd')
def change_pswd():
    pass

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
