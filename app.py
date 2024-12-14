from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
