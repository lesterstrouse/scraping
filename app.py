from flask import Flask, render_template
import pymongo
import scrape_mars

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.scrape_db
collection = db.scrape_data

@app.route("/scrape")
def scrape_call():
    scrapes = db.scrape_data
    scrapes.delete_many({})
    data = scrape_mars.scrape()
    scrapes.insert_one(data)
    return "OK"

@app.route("/")
def index():
    # write a statement that finds all the items in the db and sets it to a variable
    scrape_data = db.scrape_data
    html_pass = scrape_data.find_one()
    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", html_pass = html_pass)


if __name__ == "__main__":
    app.run(debug=True)