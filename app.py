from flask import Flask, jsonify, render_template, redirect
from flask_pymongo import PyMongo
import scrapefunction

# Initialize Flask
app = Flask(__name__)

# Initialize MongoDB, name database
mongo = PyMongo(app, uri="mongodb://localhost:27017/sail_db")

# Query MongoDB document and pass its data into HTML
@app.route("/")
def index():
    sail = mongo.db.sail_db.find_one()
    return render_template("index.html", scuttlebutt=sail)

@app.route("/scrape")
def scrape():
    # Scrape and get dictionary of scraped values from function
    sail_scraped = scrapefunction.scrape_sail_news()

    # Declare the db
    sail_db = mongo.db.sail_db

    # Insert document containing our dictionary into the db
    sail_db.update(
        {},
        sail_scraped,
        upsert=True
    )

    # Redirect to the home page
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)