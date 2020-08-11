from flask import Flask, render_template
import pymongo

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
# @app.route('/scrape')









if __name__ == "__main__":
    app.run(debug=True)

    