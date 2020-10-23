from flask import Flask
from flask import render_template, redirect, jsonify
from flask import request
from flask import session
from flask import send_from_directory

import os

from SqlController.receivetable import ReceiveData
from SqlController.userdata import UserData

app = Flask(__name__)
app.secret_key=b"19971128"
#engine=create_engine("sqlite:///sample.sqlite3")
#Base=declarative_base()

################################################################
# function
# TODO : Prepare another file.
################################################################
def isLogin():
    # session login? => (True):rerturn session id.
    if "login" in session and session["login"]:
        login_user=session["id"]
        session["login"]=True
    else:
        login_user=""
        session["login"]=False
    return session["login"], login_user

################################################################
# Page before login
################################################################
# top page.
@app.route("/")
def top_page():
    # session login check.
    islogin, loginuser=isLogin()
    # for debug
    alldata=UserData.getAll()
    if isLogin:
        # return render_template("/userpage/data.html", title="なにかのページ", all_userdata = alldata, login_flg=islogin, login_user=loginuser)
        return render_template("/index.html", title="なにかのページ", all_userdata = alldata, login_flg=islogin, login_user=loginuser)
    else:
        return render_template("/index.html", title="なにかのページ", all_userdata = alldata, login_flg=islogin, login_user=loginuser)

# information page. (Contact page to the creator)
@app.route("/information")
def author_info():
    islogin, loginuser=isLogin()
    return render_template("/information.html", title="お問い合わせ", login_flg=islogin, login_user=loginuser)

# login page.
@app.route("/login")
def login():
    return render_template("/userpage/login.html", title="ログイン", msg="", login_flg=False, login_user="")

# send login form.
@app.route("/login",methods=["POST"])
def login_post():
    # Get the id and password from the http post.
    request_id=request.form.get("id")
    request_password=request.form.get("pass")
    if(UserData.dologin(request_id, request_password)):
        # Record login information in the session.
        session["login"]=True
        session["id"]=str(request_id)
        return redirect("/")
    else:
        return render_template("/userpage/login.html", title="ログイン", msg="IDまたはパスワードが異なっています。", login_flg=False, login_user="")

@app.route("/logout")
def logout():
    session.pop("id", None)
    session.pop("login")
    return redirect("/")

# user signup page.
@app.route("/signup")
def signup():
    return render_template("/userpage/signup.html", title = "サインアップ", msg="", login_flg=False, login_user="")

# send signup data.
@app.route("/signup",methods=["POST"])
def signup_post():
    # Get the id and password and device_id from the http post.
    request_id=request.form.get("id")
    request_device_id=request.form.get("device_id")
    request_password=request.form.get("pass")
    # do database resister.
    isRegister, errormsg = UserData.makeRegistration(request_id, request_device_id, request_password)
    if(isRegister):
        # Record login information in the session.
        session["login"]=True
        session["id"]=str(request_id)
        return redirect("/")
    else:
        return render_template("/userpage/signup.html", title = "サインアップ", msg=errormsg, login_flg=False, login_user="")

@app.route("/userdata")
def userdata():
    islogin, loginuser=isLogin()
    return render_template("/userpage/userdata.html", title = str(loginuser) + "さんのぺーじ",login_flg=islogin, login_user=loginuser)

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

################################################################
# Callback for favicon.ino (does google chrome require it?)
################################################################
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

################################################################
# Flask access error.
################################################################
@app.errorhandler(404)
def page_not_found(error):
    return render_template('/error/404.html')

################################################################
# application runnning.
################################################################
if __name__ == "__main__":
    # debug mode.
    app.run(debug=True)
    # test server create
    #app.run(debug=False, host='0.0.0.0', port=80)