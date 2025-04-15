from flask import *
import printPDF
import editPDF
import urllib
import waitress

app = Flask(__name__)

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file('favicons/favicon.ico')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_reciept", methods=["POST"])
def post_print():
    form = request.form
    name = form["name"]
    price = form["price"]
    date = form["date"]
    description = form["description"]
    print(name)
    print(price)
    print(date)
    print(description)
    filename = editPDF.create_reciept(name, price, description, date)
    data = {
        "status" : "success",
        "filename" : filename
    }
    return jsonify(data)

@app.route("/print_reciept", methods=["POST"])
def print_reciept():
    form = request.form
    filename = form["filename"]
    print(filename)
    is_success = printPDF.print_pdf(filename)
    data = {
        "status": "success",
        "success" : is_success,
        "filename" : filename
    }
    return jsonify(data)

@app.route("/reprint")
def reprint():
    return render_template("reprint.html")

if __name__ == "__main__":
    waitress.serve(app,port=8080,host="0.0.0.0", threads=4)