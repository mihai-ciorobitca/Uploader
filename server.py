from flask import Flask, request, session, \
    redirect, url_for, render_template, \
    jsonify, send_from_directory
from dotenv import load_dotenv
import os

load_dotenv('.env')

SECRET_KEY = os.getenv("SECRET_KEY")

website = Flask(__name__)
website.secret_key = SECRET_KEY
website.config['UPLOAD_FOLDER'] = "uploads"


@website.errorhandler(404)
def page_not_found(e):
    return redirect(url_for("index"))


@website.route('/')
def index():
    return redirect(url_for("home"))


@website.route('/home', methods=['GET', 'POST'])
def home():
    if session.get("user", False):
        if request.method == 'POST':
            if 'file' not in request.files:
                return render_template("home.html")
            file = request.files['file']
            if file.filename == '':
                return render_template("home.html")
            file.save(
                os.path.join(
                    website.config['UPLOAD_FOLDER'],
                    file.filename)
            )
            return jsonify({"status": "success", "message": "File uploaded successfully"})
        return render_template("home.html")
    return redirect(url_for("login"))


@website.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if (username, password) == ("username", "password"):
            session["user"] = True
            return redirect(url_for("home"))
        elif (username, password) == ("admin", "admin"):
            session["admin"] = True
            return redirect(url_for("admin"))
    return render_template("login.html")


@website.route("/admin")
def admin():
    if session.get("admin",False):
        files = os.listdir("uploads")
        return render_template(
            "admin.html",
            files=files
        )
    return redirect(url_for("login"))

@website.route('/download/<filename>')
def download(filename):
    return send_from_directory(
        "uploads",
        filename
    )


if __name__ == "__main__":
    website.run(
        host='0.0.0.0',
        port=5000
    )
