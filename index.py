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

@app.route('/admin_portal')
def index():
	if seesion.get('admin_id'):
		return render_template('admin_portal.html',
			logged_in = [session['admin_id'], session['admin_info']])
	else:
		return render_template('admin_login.html')

@app.route('/register', methods=['POST'])
def register():
	return render_template('register.html')

if (__name__) == "__main__":
	app.run(debug=True)