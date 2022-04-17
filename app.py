# pip install flask 
# pip install flask_pymongo -user
# pip install dnspython -user
# python -m pip install 'pymongo[srv]'
# install bcrypt
import secrets
from flask import Flask, session, url_for
from flask import render_template
from flask import request, redirect
from flask_pymongo import PyMongo
from model import topics
from blog_models import blog_topics
import bcrypt
from bson.objectid import ObjectId
import os 


# Initialization section
app = Flask(__name__)

# Name of database
app.config['MONGO_DBNAME'] = 'myblog'

# URI of database
app.config['MONGO_URI'] = "mongodb+srv://admin:OIERxhVZ2WPIJfdw@cluster0.phikc.mongodb.net/myblog?retryWrites=true&w=majority"
# app.config["MONGO_URI"] = "mongodb://localhost:27017/visipedia_annotation_toolkit"
# print(os.environ.get('MONGO_URI'))
# app.config['MONGO_URI'] = os.environ.get('MONGO_URI')

# For using session object
app.secret_key = secrets.token_urlsafe(16)

# Initialize PyMongo
mongo = PyMongo(app)

# mongo.db.create_collection("blogs")
# mongo.db.create_collection("users")

# Routes Section

@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')

    result = "result"
    return render_template("index.html", result=result)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route ("/contact")
def contact():
    return render_template('contact.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"].encode("utf-8")

        lookedup_user = mongo.db.users.find_one({"name":username})

        if lookedup_user:
            if bcrypt.checkpw(password, lookedup_user["password"]):
                session["username"] = username
                required_blog = list(mongo.db.blogs.find({}))
                has_blog = True if len(required_blog) > 0 else False  
                return render_template("all.html", required_blog=required_blog, topics=topics, has_blog=has_blog)
            else:
                return "Incorrect Password"
        else:
            return "Username doesn't exist"
    else:
        return render_template('login.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        # search the username in database
        existing_user = users.find_one({'name': request.form['username']})

        # if user not in database
        if not existing_user:
            username = request.form['username']
            # takes string and converts to binary array 
            password = request.form['password'].encode("utf-8")

            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password, salt)
            
            # add new user to database
            users.insert_one({'name':username, 'password':hashed_password})
            # store username in session
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return "Username already registered. Try logging in. It you still want to signup, try with another username."
    else:
        return render_template("signup.html")

# Logout Route
@app.route('/logout')
def logout():
    # clear the username from the session data
    session.clear()
    return redirect('/')

@app.route("/featured")
def featured_blog():
    return render_template("featured.html")

@app.route("/all", methods=['GET', 'POST'])
def all_blogs():
    # mongo.db.blogs.insert_many(blog_topics)

    required_blog = list(mongo.db.blogs.find({}))
    has_blog = True if len(required_blog) > 0 else False  
    return render_template("all.html", required_blog=required_blog, topics=topics, has_blog=has_blog)

@app.route("/<topic>")
def blog_topic(topic):
    required_blog = list(mongo.db.blogs.find({'topic':topic}))
    has_blog = True if len(required_blog) > 0 else False  
    return render_template('all.html', required_blog=required_blog, topics=topics, has_blog=has_blog)

# @app.route("/add" ,methods=['GET','POST'])
# def add():
#     if request.method == 'GET':
#         return render_template('all.html', topics=topics)
#     else:
#         if request.form['name'] == '' or request.form['topic'] == '' or request.form['description'] == '':
#             return render_template('add.html', topics=topics, failed_attempts=True)
#         name = request.form['name'] 
#         topic = request.form['topic']
#         description = request.form['description']

#         collection = mongo.db.blogs

#         # insert an entry to the database
#         collection.insert_one({'name':name, 'topic':topic, 'description':description})

#         # redirect to the all route upon form submission
#         return redirect('/all')

# blog variable route
@app.route('/blog/<blogID>')
def blog_view(blogID):
    collection = mongo.db.blogs
    # find single entry by ObjectId
    blog = collection.find_one({"_id":ObjectId(blogID)})
    return render_template('blog.html', blog=blog)

# Add image route
@app.route('/blog/<blogID>/add_image', methods=['GET', 'POST'])
def add_image(blogID):
    if request.method == 'GET':
        collection = mongo.db.blogs
        # Find a single entry by ObjectId
        blog = collection.find_one({"_id":ObjectId(blogID)})
        return render_template('add_image.html', blog=blog)
    else:
        url = request.form["url"]
        collection = mongo.db.blogs
        blog = {"_id":ObjectId(blogID)}
        newvalues = {"$set": {"image": url}}

        collection.update_one(blog, newvalues)
        return redirect('/blog/'+blogID  )


@app.route("/feedback")
def feedback():
    return render_template("feedback.html")


if __name__ == "__main__":
    app.run()