from flask import Flask, render_template , request, url_for ,redirect , session , flash
from flask_mail import Mail, Message
import pymysql


app = Flask(__name__)
app.secret_key = 'Any string'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'hayhaytutor@gmail.com'
app.config['MAIL_PASSWORD'] = '$1000usd'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail=Mail(app)

db = pymysql.connect("localhost", "root", "1234", "parent")

@app.route("/index")
@app.route("/email")
def email():
   msg = Message('Instrutor', sender = 'hayhaytutor@gmail.com', recipients = ['haytoniky@gmail.com'])
   msg.body = "John is year 3 student of City University of Hong Kong. He got 5** Chinese in HKDSE. He can provide the materials to the students.""Plaese contact 54239802 if you interested."
   mail.send(msg)
   return "Sent"+ '<br>' + "<a href = '/success'>Click Here to back the page</a>"
   return render_template('email')

@app.route("/signup", methods = ['POST', 'GET'])
def signup():
	error = None
	if request.method == 'POST':
		usrname = request.form["username"]
		pwd =  request.form['password']
		mail=  request.form['email']
		cnumber = request.form["contactnumber"]
		ares = request.form["areas"]
		restate = request.form["residentialestate"]
		sgender = request.form["studentgender"]
		salay = request.form["salary"]
		yers = request.form["years"]
		subjct = request.form["subject"]
		wek = request.form["week"]
		hous = request.form["hour"]
		speial = request.form["special"]

		#prepare a cursor object using cursor() method
		cursor = db.cursor()

		cursor.execute("""INSERT INTO user (username, password, email, contactnumber, areas, residentialestate, studentgender,
			salary, years, subject, week, hour, special) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (usrname, pwd, 
				mail, cnumber, ares, restate, sgender, salay, yers, subjct, wek, hous, speial))

		db.commit()	
	else:
		flash('You have registered and can log in, success')

	return render_template("signup.html", error = error)
	db.close()

@app.route("/login", methods = ['POST', 'GET'])
def login():
	error = None
	if request.method == 'POST':
		usrname = request.form["username"]
		pwd = request.form['password']
		custName=[]
		custPassword=[]

		db = pymysql.connect("localhost", "root", "1234", "parent")


		#
		cursor = db.cursor()

		#
		#
		sql = ("SELECT username, password FROM user WHERE username = '"+usrname+"'")
		cursor.execute(sql)
		#
		db.commit()
		results = cursor.fetchall()
		for row in results:
			custName = row[0]
			custPassword = row[1]
			#
		if custName ==[]:
			return render_template("login.html", test="Wrong username and password")

		if str((usrname == custName[0])) and str((pwd == custPassword[0])):
			return redirect(url_for('success', guest = custName))

		elif str((usrname == custName[0])) and str((pwd!= custPassword[0])):
			return render_template("login.html", test="Wrong password")


	return render_template("login.html", error = error)

@app.route("/guest/<guest>")
def parent(guest):
	return 'Hello %s! as Guest' % guest + '<br>' + "<a href = '/logout'>Click Here to log out</a>" + '<br>' + "<a href = '/home'>Click Here to home page</a>"

@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/question")
def question():
	return render_template("question.html")

@app.route("/aboutus")
def aboutus():
	return render_template("aboutus.html")

@app.route("/reference")
def reference():
	return render_template("reference.html")

@app.route("/success", methods=['GET', 'POST'])
def success():
	return render_template("success.html")

@app.route("/instructor")
def instructor():
	return render_template("instructor.html")

@app.route("/contactus", methods = ['POST', 'GET'])
def contactus():
	error = None
	if request.method == 'POST':
		nme = request.form["name"]
		eamil =  request.form['email']
		coment = request.form["comment"]
		#prepare a cursor object using cursor() method
		cursor = db.cursor()
		
		cursor.execute("""INSERT INTO comment (name, email, comment) VALUES (%s, %s, %s)""", (nme, eamil, coment))

		db.commit()
	return render_template("contactus.html",error = error)

	db.close()

@app.route("/logout")
def logout():
	#
	session.pop('username', None)
	return 'logout successfully'+ '<br>' + "<a href = '/home'>Click Here to home page</a>"

@app.route('/dashboard')
def dashboard():
	return render_template('dashoard.html')
	#


if __name__ == '__main__':
        app.debug = True
        app.run(host="0.0.0.0", port=8000)

