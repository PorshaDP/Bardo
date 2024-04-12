from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
class User(UserMixin, db.Model):
    # __tablename__ = 'users_table'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    course = db.Column(db.Integer, index=True)
    group = db.Column(db.String(10), index=True, unique=True)
    gender = db.Column(db.String(10), index=True)
    jump = db.Column(db.Integer, index=True) #прыжок
    rise = db.Column(db.Integer, index=True) #подъем
    slant =  db.Column(db.Integer, index=True) #наклон
    pullup = db.Column(db.Integer, index=True) #подтягивание
    mark = db.Column(db.String(10), index=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #образец как связывать поля

    def __repr__(self):
        return '<Student{}>'.format(self.id)

def calculate_mark(gender, jump, rise, slant, pullup):
    mark_j, mark_r, mark_s, mark_p = 0, 0, 0, 0

    if gender == "Ж":
        # Расчет оценки для женского пола
        if jump >= 188:
            mark_j = 5
        elif 173 <= jump < 188:
            mark_j = 4
        elif 157 <= jump < 173:
            mark_j = 3
        elif 142 <= jump < 157:
            mark_j = 2
        else:
            mark_j = 1

        if rise >= 51:
            mark_r = 5
        elif 41 <= rise < 51:
            mark_r = 4
        elif 35 <= rise < 41:
            mark_r = 3
        elif 25 <= rise < 35:
            mark_r = 2
        else:
            mark_r = 1

        if slant >= 13:
            mark_s = 5
        elif 8 <= slant < 13:
            mark_s = 4
        elif 6 <= slant < 8:
            mark_s = 3
        elif 3 <= slant < 6:
            mark_s = 2
        else:
            mark_s = 1

        if pullup >= 15:
            mark_p = 5
        elif 12 <= pullup < 15:
            mark_p = 4
        elif 8 <= pullup < 12:
            mark_p = 3
        elif 5 <= pullup < 8:
            mark_p = 2
        else:
            mark_p = 1

    # elif gender == "М":
        # Расчет оценки для мужского пола
        # Добавьте код для расчета оценки на основе параметров прыжка, подъема, наклона и подтягивания для мужского пола

    # Расчет средней оценки
    average = (mark_j + mark_r + mark_s + mark_p) / 4

    return average