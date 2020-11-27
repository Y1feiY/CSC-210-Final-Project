from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
application = app
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diet.db'

db = SQLAlchemy(app)

@app.route('/', methods=['POST', 'GET'])
def index():
	return render_template('main.html')