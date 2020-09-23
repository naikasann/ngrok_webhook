from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def top_page():
    # TODO : html create.
    return render_template('top_page.html', title='test server')

@app.route("/user/<name>")
def user_data():
    # TODO : You can view details of the user's information.
    # TODO : html create.
    # NOW => error ;<
    return render_template('user.html', title='test server')

@app.route("/data_form", methods=["POST"])
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

## おまじない
if __name__ == "__main__":
    app.run(debug=True)