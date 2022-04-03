# pip install flask 
# pip install flask_pymongo -user
# pip install dnspython -user
# python -m pip install 'pymongo[srv]'
from flask import Flask
from flask import render_template
from flask import request, redirect
from flask_pymongo import PyMongo

# Initialization section
app = Flask(__name__)

# Name of database
app.config['MONGO_DBNAME'] = 'myblog'

# URI of database
app.config['MONGO_URI'] = "mongodb+srv://admin:OIERxhVZ2WPIJfdw@cluster0.phikc.mongodb.net/myblog?retryWrites=true&w=majority"

# Initialize PyMongo
mongo = PyMongo(app)

# mongo.db.create_collection("blogs")


# Routes Section

@app.route("/")
@app.route("/home")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/login")
def login():

    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/featured")
def featured_blog():
    return render_template("featured.html")

@app.route("/all")
def all_blogs():
    return render_template("all.html")

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")


if __name__ == "__main__":
    app.run()