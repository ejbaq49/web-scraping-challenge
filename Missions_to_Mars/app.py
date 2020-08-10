from flask import Flask, render_template
import pymongo

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection

# add home route

# add scrape route










if __name__ == "__main__":
    app.run(debug=True)

    