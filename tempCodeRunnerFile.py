from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_mysqldb import MySQL
import bcrypt
from MySQLdb.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(app)
app.secret_key = 'key'  # Secret key for sessions

# MySQL Configurations
app.config['MYSQL_HOST'] = 'localhost'  # Your MySQL server address
app.config['MYSQL_USER'] = 'root'       # MySQL username
app.config['MYSQL_PASSWORD'] = ''  # Your MySQL password
app.config['MYSQL_DB'] = 'pizzeria'  # The name of your database

# Home route
@app.route('/')
def home():
    user = None

    if 'user_id' in session:
        cursor = mysql.connection.cursor(DictCursor)
        cursor.execute("SELECT * FROM users WHERE id=%s", (session['user_id'],))
        user = cursor.fetchone()
        cursor.close()

        session['user'] = {
            'username': user['name'],
            'email': user['email']
        }
    
    return render_template('home.html', user=user)

# Menu route
@app.route('/menu')
def menu():
    return render_template('menu.html', title="Our Menu")

# About route
@app.route('/about')
def about():
    return render_template('about.html', title="About Us")

# Contact route
@app.route('/contact')
def contact():
    return render_template('contact.html', title="Contact Us")

# Register Form
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

# Login Route
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
        
        # Verify user and password using bcrypt
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['user_id'] = user['id']  # Store user ID in session
            flash("Veiksmīgi pieteicies!", "success")
            return redirect(url_for('home'))
        else:
            flash("E-pasts vai parole ir nepareizi.", "error")

    return render_template('login.html', form=form)

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE email=%s", (form.email.data,))
        if cursor.fetchone():
            flash("E-pasts jau ir reģistrēts!", "danger")
            return redirect(url_for('register'))
        
        # Hashing password with bcrypt
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Inserting user into the database
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                       (form.name.data, form.email.data, hashed_password))
        mysql.connection.commit()
        user_id = cursor.lastrowid  # Fetch the new user's ID
        cursor.close()
        
        # Automatically log in the user
        session['user_id'] = user_id
        flash("Reģistrācija veiksmīga! Jūs esat automātiski pieslēgts.", "success")
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

# Logout Route
@app.route('/logout')
def logout():
    session.clear()
    flash("Jūs esat veiksmīgi izrakstījies.", "info")
    return redirect(url_for('home'))

# Main
if __name__ == '__main__':
    app.run(debug=True)
