from flask import Flask, render_template, redirect
import pymongo
from scrape import scrape_planet


app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.planet_db
planet_coll = db.planet_data

# add home route
@app.route('/')
def home():
    results = planet_coll.find_one()
    # pass data to template html
    return render_template('index.html', results=results)


# add scrape route
@app.route('/scrape')
def freshen_data():
    # scrape for new data
    scrape_planet()
    # return to home route
    return redirect("/", code=302)




if __name__ == "__main__":
    app.run(debug=True)

    