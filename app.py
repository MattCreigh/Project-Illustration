
### IMPORTS ################################################################################

from flask import Flask, render_template, redirect, url_for, request
from testLib import *

### APP-CONFIG #############################################################################

app = Flask(__name__)


### ROUTE FOR LOGIN ########################################################################

@app.route("/", methods=["GET","POST"])

def login():
    return render_template("login.html")

### SERVER INIT ###########################################################################

if __name__ == "__main__":
    app.run(debug = True)

### END OF CODE ############################################################################
