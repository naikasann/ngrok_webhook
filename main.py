from flask import Flask
from flask import render_template, redirect, jsonify
from flask import request
from flask import session
from flask import send_from_directory

import os
import json
import datetime

from Database.users import Users
from Database.postdatas import PostDatas
from Database.gpsdatas import GpsDatas

app = Flask(__name__)
app.secret_key=b"888888"
#engine=create_engine("sqlite:///sample.sqlite3")
#Base=declarative_base()

################################################################
# function
# TODO : Prepare another file.
################################################################
def isLogin():
    # session login? => (True):rerturn session id.
    if "login" in session and session["login"]:
        islogin=True
    else:
        islogin=False
    return islogin

def get_username(islogin):
    if islogin:
        name = session["id"]
    else:
        name = ""
    return name

################################################################
# Page before login
################################################################
# top page.
@app.route("/debug")
def debug_page():
    alldata=Users.getAll()
    print("alldata", alldata)
    return render_template("/debug.html", title="なにかのページ", all_userdata=alldata)

# top page.
@app.route("/")
def top_page():
    # session login check.
    if isLogin():
        alldata=PostDatas.getAll()
        return render_template("/userpage/data.html", title="なにかのページ", all_userdata=alldata, login_flg=True, login_user=get_username(True))
    else:
        return redirect("/login")

# information page. (Contact page to the creator)
@app.route("/information")
def author_info():
    return render_template("/information.html", title="お問い合わせ", login_flg=isLogin(), login_user=get_username(isLogin()))

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
    if(Users.doLogin(request_id, request_password)):
        # Record login information in the session.
        session["login"]=True
        session["id"]=str(request_id)
        return redirect("/")
    else:
        return render_template("/userpage/login.html", title="ログイン", msg="IDまたはパスワードが異なっています。", login_flg=False, login_user="")

@app.route("/logout")
def logout():
    session.pop("id", None)
    session.pop("login", False)
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
    isRegister, errormsg = Users.makeRegistration(request_id, request_device_id, request_password)
    if(isRegister):
        # Record login information in the session.
        session["login"]=True
        session["id"]=str(request_id)
        return redirect("/")
    else:
        return render_template("/userpage/signup.html", title = "サインアップ", msg=errormsg, login_flg=False, login_user="")

@app.route("/userdata")
def userdata():
    return render_template("/userpage/userdata.html", title = str(get_username(isLogin())) + "さんのぺーじ",login_flg=isLogin(), login_user=get_username(isLogin()))

################################################################
# Http request page.
################################################################
@app.route("/dataform", methods = ["POST"])
def data_form():
    # communicating with the correct means of request?
    if request.method == 'POST':
        # Find out who sent it (only SIGFOX will receive it this time)
        if request.headers.get('User-Agent') == "SIGFOX":
            # Retrieve the body information and convert it to json format
            request_data = json.loads(request.data)
            # Retrieving the data needed for the database. (Device ID, receive time, actual raw data)
            device_id = request_data["device"]
            recv_time = datetime.datetime.fromtimestamp(request_data["time"])
            data = request_data["data"]
            # Extracting location information from json. If have GPS => Location information acquisition()
            if request_data["computedLocation"]["status"] == 1:
                lat, lng = (int(request_data["computedLocation"]["lat"]), int(request_data["computedLocation"]["lng"]))
                # Radius of error (meters)
                radius = int(request_data["computedLocation"]["radius"])
            else:
                # donthave => Register Null Island(joke :DDDDDDDDDDDDDDD)
                lat, lng = (0, 0)
                radius = 0
            # Add to the database => postdatas, gpsdatas, rawdatas
            PostDatas.doRecord(device_id, data, recv_time)
            dataid = PostDatas.getLastDataid()
            GpsDatas.doRecord(lat, lng, radius, dataid[0])
        else:
            # If the POST communication was from a different agent.This time you reply with a json and do nothing.
            return jsonify({'status':'It is sent by an unregistered agent. We are unable to receive it.'})

    return jsonify({'status':'OK'})

@app.route("/user_state", methods = ["POST"])
def get_user_state():
    # TODO : now last state not saved.
    if request.method == "POST":
        requeststate = "ok"
        result = "not complete this page..."
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