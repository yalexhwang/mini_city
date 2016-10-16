from flask import Flask, render_template, request, redirect, jsonify, session
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
app.secret_key = 'ALVAF34591042%&@lkjfkladfadfdaf'

@app.route('/')
def index():
	return redirect('/admin_login')

@app.route('/admin_login')
def login():
	if session.get("admin"):
			return redirect('/admin_portal')
	else:
		return render_template("admin_login.html")

@app.route('/login_submit', methods=['POST'])
def login_submit():
	username = request.form['username']
	password = request.form['password']
	login_query = "SELECT * FROM admin WHERE admin_name = '%s' and password = '%s'" % (username, password)
	cursor.execute(login_query)
	admin = cursor.fetchone()
	if admin is None:
		return render_template('admin_login.html',
			message = "Please try again.")
	else:
		session['admin'] = admin
		return redirect('/admin_portal')

@app.route('/admin_portal')
def admin_portal(): 
	container_query = "SELECT c.*, count(nfc.id) FROM containers as c INNER JOIN nfc ON nfc.container = c.id GROUP BY c.id"
	cursor.execute(container_query)
	data1 = cursor.fetchall()

	nfc_user_query = "SELECT nfc.id, nfc.nfc_tag_id, nfc.container, nfc.created_at, users.first_name, users.last_name, users.gender, users.special_status FROM nfc INNER JOIN users ON nfc.user = users.id"
	cursor.execute(nfc_user_query)
	data2 = cursor.fetchall()
	print data2

	log_query = "SELECT * from logs"
	cursor.execute(log_query)
	data3 = cursor.fetchall()

	return render_template('admin_portal.html',
				container = data1,
				nfc = data2,
				log = data3)

		
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