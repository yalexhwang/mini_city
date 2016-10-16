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
	#if method is get, redirect to admin_login
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

	user_query = "SELECT * from users"
	cursor.execute(user_query)
	data4 = cursor.fetchall()

	return render_template('admin_portal.html',
				container = data1,
				nfcs = data2,
				log = data3,
				users = data4)

#if data returned is empty, register
@app.route('/register/<id>')
def register(id):
	total_tags_query = "SELECT count(id) FROM nfc"
	cursor.execute(total_tags_query)
	total_tags = cursor.fetchone()[0]
	print "total_tags: %s" % total_tags

	container_query = "SELECT * FROM containers"
	cursor.execute(container_query)
	container = cursor.fetchall()
	print container

	duplicate_query = "SELECT id, nfc_tag_id FROM nfc WHERE nfc_tag_id = '%s'" % id
	cursor.execute(duplicate_query)
	duplicate = cursor.fetchone()
	print duplicate
	if duplicate is None:
		register_query = "INSERT INTO nfc (nfc_tag_id) values ('%s')" % id
		cursor.execute(register_query)
		conn.commit()
		return render_template('register.html',
			tag_id = id,
			total_tags = total_tags,
			container = container)
	else: 
		return render_template('register.html',
			tag_id = id,
			message = "This ID has previously been registered. Please check and try again.")


@app.route('/add_info')
def add_info():
	 return render_template('add_info.html')

@app.route('/add_info_submit', methods=['POST'])
def add_info_submit():
	tag_query = "SELECT * FROM nfc"
	cursor.execute(tag_query)
	tags = cursor.fetchall()
	num = len(tags)
	print "tag id:"
	tag_registered = tags[num-1][0]
	print tag_registered

	# tag_id = request.form['tag_id']
	fname = request.form['first_name']
	lname = request.form['last_name']
	gender = request.form.get('gender')
	# category = request.form.getlist('category')
	# print tag_id
	# print category
	# if len(category) == 0:
	# nfc_query = "INSERT INTO nfc (nfc_tag_id) values ('%s')" % tag_id
	# cursor.execute(nfc_query)
	# conn.commit()
	register_query = "INSERT INTO users (first_name, last_name, gender) values ('%s', '%s', '%s')" % (fname, lname, gender)
		# register_query = "INSERT INTO users (first_name, last_name, gender, special_status, nfc_id) values ('%s', '%s', '%s', '%s', '%s')" % (fname, lname, gender, tag_id)
	cursor.execute(register_query)
	conn.commit()

	user_id_query = "SELECT * FROM users"
	cursor.execute(user_id_query)
	users = cursor.fetchall()
	num2 = len(users)
	print 'user:'
	user_registered = users[num2-1][0]
	print user_registered

	match_query = "UPDATE nfc SET user = '%s' WHERE id = '%s'" % (user_registered, tag_registered)
	cursor.execute(match_query)
	conn.commit()
	return redirect('/admin_portal')

@app.route('/tag_log/<id>', methods=['GET'])
def tag_log(id):
	tag_id = id 
	print tag_id
	if id is None:
		return redirect('/register/' + id)
	else:
		return render_template('/tag_log/',
			tag_id = tag_id)


if (__name__) == "__main__":
	app.run(debug=True)