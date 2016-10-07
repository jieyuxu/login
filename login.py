from flask import Flask, session, render_template, request, url_for, redirect
import csv 
import hashlib

app = Flask(__name__)

storage = open("users.csv", "rb")
datab = csv.reader(storage) 
L = []
D = {}

app.secret_key = "MARSHMALLOWS"

@app.route("/")
@app.route("/login/", methods = ["POST"])
def login():
	if 'user' in session:
		return redirect(url_for("welcome"))
	return render_template('basicform.html', title="Login form")

def toD(readin):
	L = []
	D = {}
	for user in readin:
		if user:
			L.append(user)
	if L:
		for item in L:
			D[item[0]] = item[1]
	return D

@app.route("/authenticate/", methods = ["POST"])
def auth():
	storage = open("users.csv", "rb")
	datab = csv.reader(storage) #immutable reader obj
	D = toD(datab)
	user = hashlib.sha512(request.form['user']).hexdigest()
	passw = hashlib.sha512(request.form['password']).hexdigest()
	session['user'] = request.form['user']
	if user in D:
		if D[user] == passw:
			return redirect(url_for("welcome"))
	if request.form['submit'] == 'Register':
		if user in D:
			return render_template('basicform.html', title="Login form", message="Username taken")
		else:
			with open('users.csv', 'a') as file:
				file.write(user+','+passw+"\n")
		return render_template('basicform.html', title="Login form", message="Your account was created.")
	return render_template("basicform.html", message="Login failed.")

@app.route("/welcome/")
def welcome():
	return render_template("welcome.html", name= session['user'])

@app.route("/logout/")
def logout():
	session.pop('user')
	return redirect(url_for("login"))

if __name__ == "__main__":
    app.debug = True 
    app.run()




