from types import resolve_bases
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify

from SqlController.MysqlController import MysqlController


app = Flask(__name__)

@app.route("/")
def top_page():
    # TODO : html create.
    return render_template("index.html")

@app.route("/registration")
def user_registration():
    # TODO : user resistration page.
    return render_template("resistration.html")

@app.route("/user")
def user_research():
    return render_template("user_login.html")
    # TODO : user reseach page.
    # this page input id and passward => user/<name> page

@app.route("/user/<name>", methods = ["POST"])
def user_data():
    # TODO : You can view details of the user's information.
    # TODO : html create.
    # NOW => error ;<
    return render_template("user.html")

@app.route("/user_info")
def author_info():
    return render_template("user_info.html")

@app.route("/data_form", methods = ["POST"])
def data_form():
    if request.method == 'POST':
        # TODO : Register with databases and other data management systems.
        result = "ok."
    else:
        result = "dont method request."
    return jsonify({
            'status':'OK',
            'result': result
        })

@app.route("/user_state", methods = ["POST"])
def get_user_state():
    # TODO : now last state not saved.
    if request.method == "POST":
        requeststate = "ok"
        result = "not complete this page..."
        pass
    else:
        requeststate = "ng"
        result = "You are trying to enter in a way that your administrator has not yet."

    return jsonify({
        "requeststate" : requeststate,
        "result" : result
    })

# application runnning.
if __name__ == "__main__":
    app.run(debug=True)