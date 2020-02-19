from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars

app = Flask(__name__)

@app.route('/')
def home():
    mars_data = collection.find_one()
    return render_template('index.html', mars_data=mars_data)
     
@app.route('/scrape')
def scrape():
    mars_data = scrape_mars.scrape()
    # Update the mars database using update and upsert=True
    collection.update({}, mars_data, upsert=True)

    return redirect("/", code=302)
 

if __name__ == '__main__':
	app.run(debug=True)