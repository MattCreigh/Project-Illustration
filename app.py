
### IMPORTS ################################################################################

from flask import Flask, render_template


### APP-CONFIG #############################################################################

app = Flask(__name__)


### ROUTE FOR LOGIN ########################################################################

@app.route("/", methods=["GET","POST"])

def logIn():
    return render_template("home.html")


### SERVER INIT ###########################################################################

if __name__ == "__main__":
    app.run(debug = True)

### END OF CODE ############################################################################
