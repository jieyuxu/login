from flask import Flask, render_template, request
import csv 
import hashlib

app = Flask(__name__)

storage = open("users.csv", "rb")
datab = csv.reader(storage) 
L = []
D = {}

@app.route("/") 
@app.route("/login/", methods = ["POST", "GET"])
def login():
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
	if user in D:
		if D[user] == passw:
			return render_template("status.html", message="SUCCESS YOU LOGGED IN")
	if request.form['submit'] == 'Register':
		if user in D:
			return render_template('basicform.html', title="Login form", message="Username taken")
		else:
			with open('users.csv', 'a') as file:
				file.write(user+','+passw+"\n")
		return render_template('basicform.html', title="Login form", message="Your account was created.")
	return render_template("status.html", message="YOU FAILED TO LOGIN.")

if __name__ == "__main__":
    #app.debug = True 
    app.run()


