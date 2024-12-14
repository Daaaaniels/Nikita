from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_mysqldb import MySQL
import bcrypt
from MySQLdb.cursors import DictCursor
from werkzeug.security import check_password_hash

app = Flask(__name__)
mysql = MySQL(app)
app.secret_key = 'key'

app.config['MYSQL_HOST'] = 'localhost'  # Your MySQL server address
app.config['MYSQL_USER'] = 'root'       # MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Your MySQL password
app.config['MYSQL_DB'] = 'pizzeria'  # The name of your database

@app.route('/')
def home():
    return render_template('home.html', title="Welcome to Bella Pizzeria!")

@app.route('/menu')
def menu():
    return render_template('menu.html', title="Our Menu")

@app.route('/about')
def about():
    return render_template('about.html', title="About Us")

@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact Us")

class RegisterForm(FlaskForm):
    name = StringField("Vārds", validators=[DataRequired()])
    email = StringField("E-pasts", validators=[DataRequired(), Email()])
    password = PasswordField("Parole", validators=[DataRequired()])
    submit = SubmitField("Reģistrēties")

# Login Form
class LoginForm(FlaskForm):
    email = StringField("E-pasts", validators=[DataRequired(), Email()])
    password = PasswordField("Parole", validators=[DataRequired()])
    submit = SubmitField("Pieteikties")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        # Fetch user from database
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        
        # Verify user and password
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['user_id'] = user['id']  # Store user ID in session
            flash("Veiksmīgi pieteicies!", "success")
            return redirect(url_for('home'))
        else:
            flash("E-pasts vai parole ir nepareizi.", "error")

    return render_template('login.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)
