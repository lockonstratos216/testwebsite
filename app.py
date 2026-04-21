from flask import Flask, request, render_template, redirect
from pymongo import MongoClient
from datetime import datetime


app = Flask(__name__)

#connecting mongodb database
client = MongoClient("mongodb://mongo:27017/")
db = client["mydatabase"]
collection = db["inputs"]

@app.route("/")
#this is where we bring the html file
def index():
    return render_template("index.html")

#submit string entries
@app.route("/submit", methods=["POST"])
def submit():
    user_input = request.form.get("user_input")

    if not user_input or user_input.strip() == "":
        return redirect("/")

    # Insert new entry
    collection.insert_one({
        "input": user_input,
        "time": datetime.now()
    })

    #Limit to 100 entries delete the oldest entry if exceeded 100
    if collection.count_documents({}) > 100:
        collection.delete_one({}, sort=[("_id", 1)]) 

    return redirect("/")

@app.route("/data")
def data():
    # last data entered shows up first
    data = list(collection.find().sort("_id", -1))  
    # a quick view of string input taken since the creation of containers
    return render_template("data.html", data=data)  


if __name__ == "__main__":
    #run at localhost
    app.run(debug=True, host="0.0.0.0")