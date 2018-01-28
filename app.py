from flask import Flask, jsonify, render_template
import pymongo

app = Flask(__name__)

conn = "mongodb://localhost:5000"
client = pymongo.MongoClient(conn)  
db = client.mars_data
collection = db.mars_data

db.collection.insert(mars_dictionary)

@app.route("/scrape")
def scrape():
    import scrape_mars
    return mars_dictionary
    mars_data = list(db.collection.find())
    print(mars_data)
    return render_template("index.html", mars_data=mars_data)

if __name__ == "__main__":
    app.run(debug=True)
