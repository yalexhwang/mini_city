from flask import Flask, render_template, request, redirect, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__) 
mysql = MySQL() 
app.config['MYSQL_DATABASE_USER'] = 'x'
app.config['MYSQL_DATABASE_PASSWORD'] = 'x' 
app.config['MYSQL_DATABASE_DB'] = 'mini_city'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1' 
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route('/')
def index():
	print "index"
	return 'hey'

@app.route('/register')
def register():
	 return render_template('register.html')

@app.route('/register_submit', methods=['POST'])
def register_submit():
	tag_id = request.form['tag_id']
	fname = request.form['first_name']
	lname = request.form['last_name']
	gender = request.form.get('gender')
	category = request.form.getlist('category')
	print tag_id
	print fname
	print lname
	print gender
	print category
	return "works"

@app.route('/tag_log/<id>', methods=['GET'])
def tag_log(id):
	tag_id = id 
	print tag_id
	return tag_id


if (__name__) == "__main__":
	app.run(debug=True)