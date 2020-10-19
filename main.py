from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from flask import session
from flask import redirect, url_for
from flask import send_from_directory

from types import resolve_bases

from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.visitors import traverse_using

import os

from SqlController.receivetable import ReceiveData
from SqlController.userdata import UserData

app = Flask(__name__)
app.secret_key = b"19971128"
#engine=create_engine("sqlite:///sample.sqlite3")
#Base=declarative_base()

################################################################
# function
# TODO : Prepare another file.
################################################################
def isLogin():
    # session login? => (True):rerturn session id.
    if "login" in session and session["login"]:
        login_user = session["id"]
        session["login"] = True
    else:
        login_user  = ""
        session["login"] = False
    return session["login"], login_user

################################################################
# html page.
################################################################
# top page.
@app.route("/")
def top_page():
    # for debug
    alldata=UserData.getAll()
    # session login check.
    islogin, loginuser = isLogin()
    return render_template("/index.html", all_userdata = alldata, login = islogin, login_user = loginuser)

# information page. (Contact page to the creator)
@app.route("/information")
def author_info():
    islogin, loginuser = isLogin()
    return render_template("/information.html", login = islogin, login_user = loginuser)

# login page.
@app.route("/login")
def user_research():
    return render_template("user_login.html")

# send login form.
@app.route("/login",methods=["POST"])#ログイン承認？IDとパスワードがあっていれば
def login():#承認処理
    request_id=request.form.get("id")
    request_password=request.form.get("pass")
    engine=create_engine("sqlite:///database.sqlite3")
    Session=sessionmaker(bind=engine)
    ses=Session()
    temp=ses.query(UserData).filter(UserData.id==request_id).all()
    for i in temp:
        if str(i.password)==str(request_password):   #str()にしておかないとログインできない
            all_data=ses.query(ReceiveData).filter(ReceiveData.device_id==i.device_id).all()
            ses.close()
            return render_template("userpage.html",all_data=all_data)
    ses.close()
    return render_template("index.html",log="IDまたはパスワードが違います")#とりあえずトップページ

# user signup page.
@app.route("/sign_up")
def user_registration():
    return render_template("/resistration.html")

# send signup data.
@app.route("/sign_up",methods=["POST"])#登録する
def sign_up():
    #データがタブっていなけばログインできる
    request_id=request.form.get("id")
    request_device_id=request.form.get("device_id")
    request_password=request.form.get("pass")
    userdata=UserData(id=request_id,device_id=request_device_id,password=request_password)
    engine=create_engine("sqlite:///database.sqlite3")
    Session=sessionmaker(bind=engine)
    ses=Session()
    if(len(ses.query(UserData).filter(UserData.id==request_id).all())>=1):
        ses.close()
        return render_template("index.html",log="IDが重複しています")
    ses.add(userdata)
    ses.commit()
    ses.close()
    #userdata.add()
    return render_template("index.html",log="登録成功")

################################################################
# Information page after login
################################################################
@app.route("/userpage")
def userpage():
    return render_template("userpage.html")

@app.route("/graph")
def graph():
    return render_template("graphdata.html")
################################################################
# Http request page.
################################################################
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

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

################################################################
# Flask access error.
################################################################
@app.errorhandler(404)
def page_not_found(error):
    return render_template('/error/error.html')

# application runnning.
if __name__ == "__main__":
    # debug mode.
    app.run(debug=True)
    # test server create
    #app.run(debug=False, host='0.0.0.0', port=80)