
### IMPORTS ################################################################################

from flask import Flask, render_template, redirect, url_for, request, flash
from wtforms import Form, StringField, PasswordField, validators
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from testLib import *

### APP-CONFIG #############################################################################

app = Flask(__name__)

mysql = MySQL(app)

### MySQL-CONFIG ############################################################################

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "H1nchley"
app.config["MYSQL_DB"] = "schema2"
app.config["MYSQL_HOST"] = "localhost"


### SECRET KEY #############################################################################

app.secret_key = "6d61374da4b4df53c6f8fbf4c9b05576d647a07da7498b400abaf7e1f4f44124"


### ROUTE FOR LOGIN ########################################################################

@app.route("/", methods=["GET","POST"])

def login():
    form = LogInForm(request.form)
    if request.method == "POST" and form.validate():
            log("UserName", form.UserName.data)
            try:
                cur = mysql.connection.cursor()
                cur.execute("""SELECT * FROM trunk_user_index WHERE userName = "%s";""" %form.UserName.data)
                userIndex = cur.fetchone()
                cur.close()
                if sha256_crypt.verify(form.Password.data, (userIndex[2])):
                    return redirect(url_for("profile"))
                else:
                    flash(" Incorrect Username or Password!!!")
                    return redirect(url_for("login",))
            except:
                flash(" Incorrect Username or Password!!!")
                return redirect(url_for("login",))
    return render_template("login.html", form=form)

class LogInForm(Form):
    UserName = StringField(u"UserName", validators = [validators.input_required(message="You forgot to enter your Username!") ,
    validators.Length(min = 4, max=20, message="Usernames are between 4 and 20 characters long")])

    Password = PasswordField(u"Password", validators = [validators.input_required(message="You forgot to enter your password!"),
    validators.Length(min=5, max=20, message="Passwords are between 4 and 20 characters long")])

### ROUTE FOR PROFILE ########################################################################

@app.route("/profile", methods=["GET","POST"])

def profile():
    return render_template("profile.html")



### SERVER INIT ###########################################################################

if __name__ == "__main__":
    app.run(debug = True)

### END OF CODE ############################################################################
