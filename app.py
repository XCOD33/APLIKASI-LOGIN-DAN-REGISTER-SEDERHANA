from flask import Flask, render_template, request, session, redirect, url_for
from flask_mysqldb import MySQL
import base64

app = Flask(__name__)
# secret key
app.secret_key = 'nunuk_nuvita'
# config mysql
app.config["MYSQL_HOST"] = 'localhost'
app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = ''
app.config["MYSQL_DB"] = 'login-register-project-rwp-11'

# init mysql
mysql = MySQL(app)



@app.route("/", methods = ["GET","POST"])
def home():
    if request.method == 'GET' and "loggedin" in session:

        # get all users
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user")
        users = cur.fetchall()

        return render_template('landing.html', users=users)
    if request.method == 'POST':
        if "signup-name" in request.form:


            errorSignUp = None

            name = request.form["signup-name"]
            email = request.form["signup-email"]
            password = request.form["signup-password"]
            passwordConfirm = request.form["signup-password-confirm"]

            if password != passwordConfirm:
                errorSignUp = "Your Password doesn't match"
                return render_template("login.html", errorSignUp=errorSignUp)

            # encode password
            password = request.form["signup-password"]
            password_bytes = password.encode("ascii")
            base64_bytes = base64.b64encode(password_bytes)
            base64_password = base64_bytes.decode('ascii')

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user (email, password, name) VALUES (%s, %s, %s)", (email, base64_password, name))
            mysql.connection.commit()
            cur.close()
            
            return render_template("login.html", successSignUp = "Successfully Registered")

        else:
            email = request.form["login-email"]
            password = request.form["login-password"]

            # encode password and compare it
            password_bytes = password.encode("ascii")
            base64_bytes = base64.b64encode(password_bytes)
            base64_password = base64_bytes.decode('ascii')

            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, base64_password))

            user = cur.fetchone()

            errorSignIn = None

            if user:
                session['loggedin'] = True
                session['name'] = user[3]
                session['email'] = user[1]
                return render_template('landing.html')
            else:
                errorSignIn = "Invalid Credentials"
                return render_template("login.html", errorSignIn=errorSignIn)
    else:
        return render_template('login.html')
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)