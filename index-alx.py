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
	return render_template('/admin_login.html')

@app.route('/login')
def login():
	if request.args.get("message"):
			return render_template("admin_login.html", 
					message = "Login Failed"
				)
	else:
		return render_template("admin_login.html")

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
@app.route('/register')
def register():
	#generate serial number and assign
	return "test"
	#add to databse


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