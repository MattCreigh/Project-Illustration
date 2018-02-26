
### IMPORTS ################################################################################

from flask import Flask, render_template, redirect, url_for, request, flash, session
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
    try :
        if session["logged"] == True:
            return redirect(url_for("profile"))
    except:
        form = LogInForm(request.form)
        if request.method == "POST" and form.validate():
            try:
                cur = mysql.connection.cursor()
                cur.execute("""SELECT * FROM trunk_user_index WHERE userName = "%s";""" %str(form.UserName.data))
                userIndex = cur.fetchone()
                cur.close()
                log("password", (userIndex)[2])
                if sha256_crypt.verify(form.Password.data, (userIndex[2])):
                    session["logged"] = True
                    session["username"] = form.UserName.data
                    session["userID"] = cur.fetchmany(0)
                    return redirect(url_for("profile"))
                else:
                    flash(" Incorrect username or password!!!")
                    return redirect(url_for("login"))
            except:
                flash(" Incorrect username or password!!!")
                return redirect(url_for("login",))
        return render_template("login.html", form=form)
    return render_template("login.html", form=form)

class LogInForm(Form):
    UserName = StringField(u"UserName", validators = [validators.input_required(message="You forgot to enter your Username!") ,
    validators.Length(min = 4, max=20, message="Usernames are between 4 and 20 characters long")])

    Password = PasswordField(u"Password", validators = [validators.input_required(message="You forgot to enter your password!"),
    validators.Length(min=5, max=20, message="Passwords are between 4 and 20 characters long")])

### ROUTE FOR PROFILE ########################################################################

@app.route("/profile", methods=["GET","POST"])

def profile():
    if "logged" in session:
        return render_template("profile.html")
    else:
        return redirect(url_for("login"))


### LOGOUT ROUTE ###########################################################################

@app.route("/logout", methods=["GET", "POST"])

def logOut():
    if "logged" in session:
        session.pop("logged")
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))



### SERVER INIT ###########################################################################

if __name__ == "__main__":
    app.run(debug = True)

### END OF CODE ############################################################################
