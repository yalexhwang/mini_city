from flask import Flask, render_template, request, redirect, jsonify, session
from flaskext.mysql import MySQL

app = Flask(__name__) 
mysql = MySQL() 
app.config['MYSQL_DATABASE_USER'] = 'ghdbteam12'
app.config['MYSQL_DATABASE_PASSWORD'] = 'S3yVUPXW!a^QG01@1' 
app.config['MYSQL_DATABASE_DB'] = 'ghdbteam12'
app.config['MYSQL_DATABASE_HOST'] = 'ghdb.goodiehack.com'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

@app.route('/')
def index():
	print "index"
	return render_template('/admin_login.html')

@app.route('/login')
def login():
	if session.get("admin_id"):
			return render_template("admin_login.html", 
					admin_id = admin
				)
	else:
		return render_template("admin_login.html")

@app.route('/login_submit')
def login_submit():
	username = request.form['username']
	password = request.form['password']
	print username
	print password
	login_query = "SELECT * FROM admin WHERE admin_name = '%s' and password = '%s'" % (username, password)
	cursor.execute(login_query)
	admin = cursor.fetchone()
	if admin is None:
		return redirect('/login')
	else:
		session['admin'] = admin[0]
		return render_template('/admin_portal.html',
			admin = admin[0])

@app.route('/admin_portal')
def admin_portal(): 
	container_query = "SELECT * from containers"
	cursor.execute(container_query)
	containers = cursor.fetchall()

	log_query = "SELECT * from logs"
	cursor.execute(log_query)
	logs = cursor.fetchall()

	nfc_query = "SELECT * from nfc"
	cursor.execute(nfc_query)
	nfcs = cursor.fetchall()

	services_query = "SELECT * from services"
	cursor.execute(services_query)
	services = cursor.fetchall()

	users_query = "SELECT * from users"
	cursor.execute(users_query)
	users = cursor.fetchall()

	return render_template('admin_portal.html',
				containers = containers)

		
#if data returned is empty, register
@app.route('/register/<id>')
def register(id):
	print id
	register_query = "INSERT INTO nfc (nfc_id) values ('%s')" % id
	cursor.execute(register_query)
	conn.commit()
	return id


@app.route('/add_holder')
def add_holder():
	 return render_template('add_holder.html')

@app.route('/add_holder_submit', methods=['POST'])
def add_holder_submit():
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
	if len(category) == 0:
		register_query = "INSERT INTO users (first_name, last_name, gender, nfc_id) values ('%s', '%s', '%s', '%s', '%s')" % (fname, lname, gender, tag_id)
	else: 
		register_query = "INSERT INTO users (first_name, last_name, gender, special_status, nfc_id) values ('%s', '%s', '%s', '%s', '%s')" % (fname, lname, gender, tag_id)
	return "works"

@app.route('/tag_log/<id>', methods=['GET'])
def tag_log(id):
	tag_id = id 
	print tag_id
	if id is None:
	#if no data, redirect to 'register'
		return redirect('/register')
	else:
		return render_template('/tag_log/')




if (__name__) == "__main__":
	app.run(debug=True)