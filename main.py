from SqlController.receivetable import ReceiveData
from types import resolve_bases
from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from flask.globals import session
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

from sqlalchemy.orm import sessionmaker

from SqlController.userdata import UserData

app = Flask(__name__)
#engine=create_engine("sqlite:///sample.sqlite3")
#Base=declarative_base()

@app.route("/")#トップページ
def top_page():
    # TODO : html create.
    alldata=UserData.getAll()
    return render_template("index.html",all_userdata=alldata,log="")

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

@app.route("/graph")
def graph():
    return render_template("graph.html")

@app.route("/userpage")
def userpage():
    return render_template("userpage.html")

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
    request_id=request.form.get("id")
    request_password=request.form.get("pass")
    engine=create_engine("sqlite:///user.sqlite3")
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

@app.route("/sign_up",methods=["POST"])#登録する
def sign():
    #データがタブっていなけばログインできる
    request_id=request.form.get("id")
    request_device_id=request.form.get("device_id")
    request_password=request.form.get("pass")
    userdata=UserData(id=request_id,device_id=request_device_id,password=request_password)
    engine=create_engine("sqlite:///user.sqlite3")
    Session=sessionmaker(bind=engine)
    ses=Session()
    if(len(ses.query(UserData).filter(UserData.id==request_id).all())>=1):
        ses.close()
        return render_template("index.html",log="IDかぶりで登録できませんでした。")
    ses.add(userdata)
    ses.commit()
    ses.close()
    #userdata.add()
    return render_template("index.html",log="登録成功")

# application runnning.
if __name__ == "__main__":
    app.run(debug=True)