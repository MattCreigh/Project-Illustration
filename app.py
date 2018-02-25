
### IMPORTS ################################################################################

from flask import Flask, render_template, redirect, url_for, request
from testLib import *

### APP-CONFIG #############################################################################

app = Flask(__name__)


### ROUTE FOR LOGIN ########################################################################

@app.route("/", methods=["GET","POST"])

def login():
    return render_template
    form = LogInForm(request.form)
    if request.method == "POST":
            log("UserName", form.UserName.data)
            cur = mysql.connection.cursor()
            cur.execute("""SELECT * FROM trunk_user_index WHERE userName = "%s";""" %form.UserName.data)
            userIndex = cur.fetchone()
            cur.close()
            if sha256_crypt.verify(form.Password.data, (userIndex[2])):
                return redirect(url_for("profile"))
            else:
                return redirect(url_for("login"))

    return render_template("login.html", form=form)

class LogInForm(Form):
    UserName = StringField("UserName")
    Password = PasswordField("Password")

### ROUTE FOR PROFILE ########################################################################

@app.route("/profile", methods=["GET","POST"])

def profile():
    return render_template("profile.html")



### SERVER INIT ###########################################################################

if __name__ == "__main__":
    app.run(debug = True)

### END OF CODE ############################################################################
