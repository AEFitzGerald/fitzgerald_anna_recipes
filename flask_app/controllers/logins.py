from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register_user():
    print(User.validate_user_registration(request.form))
    if User.validate_user_registration(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['loginpw'])
        print(pw_hash)
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email_address': request.form['email_address'],
            "loginpw" : pw_hash
            }
        
        User.save_user_in_db(data)

    return redirect("/")


@app.route('/login_user', methods=['POST'])
def login_user():
    
    users = User.get_users_by_email(request.form)
    
    if len(users) == 0:
        flash("User with the given email does not exist.")
        return redirect("/")
    
    user = users[0]
    
    if not bcrypt.check_password_hash(user.loginpw, request.form['loginpw']):
        flash("Invalid Entry")
        return redirect('/')
    
    session['id'] = user.id
    session['first_name'] = user.first_name
    return redirect("/dashboard")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
















