from flask import Flask, render_template, redirect, session, request
# import the Connector function
from mysqlconnection import MySQLConnector
app=Flask(__name__)
# connect and store the connection in "mysql"
# note that you pass the database name to the function
mysql=MySQLConnector(app,'fullfriends')

@app.route('/')
def index():
	query = "SELECT friends.name, friends.age, DATE_FORMAT(friends.join_date,'%M %d') AS join_date, DATE_FORMAT(friends.join_date, '%Y') AS year FROM friends"
	friends = mysql.query_db(query)
	return	render_template("index.html", all_friends=friends)

@app.route('/friends', methods=['POST'])
def post():
	name = request.form['name']
	age = request.form['age']
	query = "INSERT INTO friends (friends.name,friends.age,friends.join_date) VALUES (:name, :age, NOW())"
	
	data = {
		'name': request.form['name'],
		'age':  request.form['age']
	}

	mysql.query_db(query, data)

	return redirect('/')



app.run(debug=True)