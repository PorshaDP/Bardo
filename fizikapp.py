from config import Config
from flask_login import current_user, login_user, logout_user
from app.models import User
from flask import Flask, redirect, url_for, flash, render_template
from app.forms import LoginForm
app = Flask(__name__)
app.config.from_object(Config)
var = app.config['SQLALCHEMY_DATABASE_URI']

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title="Home Page")


@app.route('/login', methods=['GET', 'POST'])
def login():
    # # if current_user.is_authenticated:
    # #     return redirect(url_for('normative'))
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.username.data).first()
    #     if user is None or not user.check_password(form.password.data):
    #         flash('Invalid username or password')
    #         return redirect(url_for('login'))
    #     login_user(user, remember=form.remember_me.data)
    #     return redirect(url_for('normative'))
    return render_template('loginform.html', title='Sign In')



@app.route('/normative')
def normative():
    return render_template('formnormative.html')

if __name__ == '__main__':
    app.run(debug=True)
