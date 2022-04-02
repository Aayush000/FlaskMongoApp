from flask import Flask
from flask import render_template
from flask import request, redirect
from flask_pymongo import PyMongo

# Initialization section
app = Flask(__name__)

# Name of database
# app.config['MONGO_DBNAME'] = 'myblog'

# URI of database
# app.config['MONGO_URI'] = "mongodb+.."

# Initialize PyMongo
# mongo = PyMongo(app)

# mongo.db.create_collection("blogs")


# Routes Section

@app.route("/")
@app.route("/index")
def index():
    return "<h1>Hi, this is Aayush<h1/>"

if __name__ == "__main__":
    app.run()