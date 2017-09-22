from flask import Flask, render_template, redirect, session, request
# import the Connector function
from mysqlconnection import MySQLConnector
app=Flask(__name__)
# connect and store the connection in "mysql"
# note that you pass the database name to the function
mysql=MySQLConnector(app,'fullfriends')

@app.route('/')
def index():
	query = "SELECT friends.id, friends.name, friends.age, DATE_FORMAT(friends.join_date,'%M %d') AS join_date, DATE_FORMAT(friends.join_date, '%Y') AS year FROM friends"
	friends = mysql.query_db(query)
	return	render_template("index.html", all_friends=friends)


@app.route('/new')
def newuser():
	return	render_template('new.html')

@app.route('/friends', methods=['POST'])
def post():
	query = "INSERT INTO friends (friends.name,friends.age,friends.join_date) VALUES (:name, :age, NOW())"
	
	data = {
		'name': request.form['name'],
		'age':  request.form['age']
	}

	mysql.query_db(query, data)

	return redirect('/')

@app.route('/<id>')
def user(id):
	query = """SELECT friends.id, friends.name, friends.age, 
	DATE_FORMAT(friends.join_date,'%M %d') AS join_date, 
	DATE_FORMAT(friends.join_date, '%Y') AS year 
	FROM friends
	WHERE friends.id = :id"""

	data ={
	"id":id
	}

	friends = mysql.query_db(query, data)

	print friends
	return render_template('user.html', all_friends=friends[0])

@app.route('/<id>/edit')
def edit(id):
	user_id = id
	return render_template('edit.html', id = user_id)
	
@app.route('/<id>/edit/alter', methods = ["POST"])
def alterdata(id):
	query = """UPDATE friends
	SET friends.name = :new_name, friends.age = :new_age
	WHERE friends.id = :id"""

	data = {
	"new_name": request.form['name'],
	"new_age": request.form['age'],
	"id" : id
	}

	print data

	mysql.query_db(query, data)

	return redirect('/')

@app.route('/<id>/delete')
def delete(id):
	query ="""DELETE FROM friends
	WHERE friends.id = :id """
	data = {
	"id": id
	}

	mysql.query_db(query, data)

	return	redirect('/')


	
app.run(debug=True)