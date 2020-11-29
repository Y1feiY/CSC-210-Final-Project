import os
from flask import Flask, render_template, request, redirect
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
application = app

# basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'hard to guess string'
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'databases.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diet.db'


db = SQLAlchemy(app)
manager = Manager(app)


class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(50), nullable=False)
	last_name = db.Column(db.String(50), nullable=False)
	weight = db.Column(db.String(50), nullable=False)
	height = db.Column(db.String(50), nullable=False)
	expected_calories = db.Column(db.String(50), nullable=False)

	# diet_plan = db.relationship('DietPlan', backref='user')


class DietPlan(db.Model):
	__tablename__ = 'diet'
	id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.String(50), nullable=False)
	morning_meal = db.Column(db.String(50), nullable=False)
	noon_meal = db.Column(db.String(50), nullable=False)
	evening_meal = db.Column(db.String(50), nullable=False)
	claories_in = db.Column(db.String(50))

	# user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	# user = db.relationship('User', backref='diet')


@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == "POST" and request.form.get("add"):
		day = request.form['day']
		morning = request.form['morning']
		noon = request.form['noon']
		evening = request.form['evening']
		calories = request.form['calories']
		day_plan = DietPlan(day=day, morning_meal=morning, noon_meal=noon, 
			evening_meal=evening, claories_in=calories)
		try:
			db.session.add(day_plan)
			db.session.commit()
			return redirect('/')
		except:
			return "There was an error adding the plan!"

	elif request.method == "POST" and request.form.get("add_user"):
		f_name = request.form['f_name']
		l_name = request.form['l_name']
		weight = request.form['weight']
		height = request.form['height']
		exp_calories = request.form['calories']
		new_user = User(first_name=f_name, last_name=l_name, weight=weight, 
			height=height, expected_calories=exp_calories)
		try:
			db.session.add(new_user)
			db.session.commit()
			return redirect('/')
		except:
			return "There was an error adding the user!"

	elif request.method == 'POST' and request.form.get("morning_update"):
		new_mor = request.form.get("new_mor")
		old_mor = request.form.get("old_mor")
		plan = DietPlan.query.filter_by(morning_meal=old_mor).first()
		plan.morning_meal = new_mor
		db.session.commit()
		return redirect('/')

	elif request.method == 'POST' and request.form.get("noon_update"):
		new_noon = request.form.get("new_noon")
		old_noon = request.form.get("old_noon")
		plan = DietPlan.query.filter_by(noon_meal=old_noon).first()
		plan.noon_meal = new_noon
		db.session.commit()
		return redirect('/')

	elif request.method == 'POST' and request.form.get("evening_update"):
		new_eve = request.form.get("new_eve")
		old_eve = request.form.get("old_eve")
		plan = DietPlan.query.filter_by(evening_meal=old_eve).first()
		plan.evening_meal = new_eve
		db.session.commit()
		return redirect('/')

	elif request.method == 'POST' and request.form.get("calories_update"):
		new_cal = request.form.get("new_cal")
		old_cal = request.form.get("old_cal")
		plan = DietPlan.query.filter_by(claories_in=old_cal).first()
		plan.claories_in = new_cal
		db.session.commit()
		return redirect('/')

	else:
		diets = DietPlan.query.all()
		users = User.query.all()
		return render_template('main.html', diets=diets, users=users)


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    plan_to_update = DietPlan.query.get_or_404(id)
    if request.method == "POST":
        plan_to_update.day = request.form['day']
        plan_to_update.morning_meal = request.form['morning']
        plan_to_update.noon_meal = request.form['noon']
        plan_to_update.evening_meal = request.form['evening']
        plan_to_update.claories_in = request.form['calories']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error updating the plan!"
    else:
        return render_template('update.html', plan_to_update=plan_to_update)


@app.route('/delete/<int:id>')
def delete(id):
    plan_to_delete = DietPlan.query.get_or_404(id)
    try:
        db.session.delete(plan_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleting the plan!"

@app.route('/delete_user/<int:id>')
def delete_user(id):
    plan_to_delete = User.query.get_or_404(id)
    try:
        db.session.delete(plan_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleting the user!"

if __name__ == '__main__':
	manager.run()