from types import resolve_bases
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from SqlController.MysqlController import MysqlController

from SqlController.userdata import UserData

app = Flask(__name__)
#engine=create_engine("sqlite:///sample.sqlite3")
#Base=declarative_base()

@app.route("/")#トップページ
def top_page():
    # TODO : html create.
    alldata=UserData.getAll()
    return render_template("index.html",all_userdata=alldata)

@app.route("/registration")#登録ページ
def user_registration():
    # TODO : user resistration page.
    return render_template("resistration.html")

@app.route("/user")#ユーザーページ
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
        print(request.form)
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
@app.route("/login",methods=["POST"])#ログイン承認？IDとパスワードがあっていれば
def test():#承認処理
    return render_template("index.html")#とりあえずトップページ
@app.route("/sign_up",methods=["POST"])#登録する
def sign():
    #データがタブっていなけばログインできる
    return render_template("index.html")
# application runnning.
if __name__ == "__main__":
    app.run(debug=True)