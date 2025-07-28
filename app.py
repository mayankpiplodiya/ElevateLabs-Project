from flask import Flask, render_template, request, redirect, url_for, session
from transformers import pipeline
import textstat

app = Flask(__name__)
app.secret_key = "secret"

users = {"admin": "admin"}

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.route("/", methods=["GET", "POST"])
def index():
    if "username" not in session:
        return redirect(url_for("login"))

    summary = ""
    word_count = 0
    readability = ""
    input_text = ""

    if request.method == "POST":
        input_text = request.form["article"]
        if len(input_text.split()) > 1000:
            summary = "Article too long! Please shorten it."
        else:
            result = summarizer(input_text, max_length=150, min_length=40, do_sample=False)
            summary = result[0]['summary_text']
            word_count = len(summary.split())
            readability = textstat.flesch_reading_ease(summary)

    return render_template("summarize.html",
                           input_text=input_text,
                           summary=summary,
                           word_count=word_count,
                           readability=readability,
                           username=session["username"])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username] == password:
            session["username"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return render_template("signup.html", error="User already exists")
        else:
            users[username] = password
            return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
