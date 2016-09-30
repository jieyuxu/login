from flask import Flask, render_template, request

app = Flask(__name__)
usr = "Amy"
password = "catscatscats"

@app.route("/") #assign following fxn to run when root route requested
@app.route("/login/")
def table_this():
	#print request.headers
	return render_template('basicform.html', title="Login form")

@app.route("/authenticate/", methods = ["POST"])
def auth():
	if request.form['user'] == usr and request.form['password'] == password:
		return render_template("status.html", message="SUCCESS YOU LOGGED IN")
	return render_template("status.html", message="YOU FAILED TO LOGIN.")
    
if __name__ == "__main__":
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()


