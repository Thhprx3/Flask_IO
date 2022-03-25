from flask import current_app as app
from flask import render_template, Flask

@app.route("/")
def home():
    return render_template("index.html", page='home')

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", page='dashboard')

@app.route("/predict")
def predict():
    return render_template("predict.html", page='predict')
