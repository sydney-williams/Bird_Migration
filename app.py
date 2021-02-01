# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
# from dotenv import load_dotenv
import os
import json
from flask import Flask, render_template, url_for

# load_dotenv()
# username=os.environ.get('DB_USERNAME')
# password=os.environ.get('DB_PASSWORD')

#Call data from postgres server
engine = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/bird_migration')

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Create our session (link) from Python to the DB
session = Session(engine)

# Request data from postgres
resultproxy = session.execute("SELECT * FROM bird_count")

# Write data into dictionary
d, a = {}, []
for rowproxy in resultproxy:
     # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
     for column, value in rowproxy.items():
         # build up the dictionary
         d = {**d, **{column: value}}
     a.append(d)   

# Flask Setup
app = Flask(__name__)
# Flask Routes

#flask app gallery
@app.route('/all')
def gallery():
    return render_template('gallery.html')


#flask app v1
@app.route('/')

def entry():
    return render_template('index.html', data = a)



# flask app map route
@app.route('/map/<species>')
def map(species):

    #Create dictionary for mapping
    regions = {0: {'name': "Central High", 'location': [36.00, -94]}, 
    1: {'name': "East Coast", 'location': [38, -75.00]}, 
    2: {'name': "Lower West Coast", 'location': [33.00, -117.00]}, 
    3: {'name': "Northern Highlands", 'location': [55.00, -64.00]}, 
    4: {'name': "Other interior highlands", 'location': [38.60, -101]}, 
    5: {'name': "Upper west coast", 'location': [45.00, -120.00]}}

    # filter bird data (a) by id as determined in route input - NEED TO CHANGE FROM TESTER "AMERICAN COOT"
    speciesFilter = list(filter(lambda d: d['SPECIESNAME'] == species, a))

    # set initial birdcount variable
    birdcount = 0

    #loop through regions array
    for region in regions:

        #loop through the filtered bird data
        for result in speciesFilter:

            # loop through birdcount data to sum totals for regions
            if result['REGION'] == regions[region]['name']:
                
                # add birdcount to counter
                birdcount = birdcount + int(result['COUNT'])

        # append key item to dictionary
        regions[region]['count']=birdcount

        #reset birdcount to 0
        birdcount= 0

    #render template
    return render_template('mapIndex.html', regions = regions)

#run app -- this needs to be at the end of the script
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5010)

# #flask app v2
# #@app.route('/data/speciesname/')
# #def access_data(speciesname):

#     # Check records for something that matches the params. This is where you would us a database query similar to HW12.
# #    results = []
# #    for record in records:
# #        key, value = speciesname.split('=')
# #        if record[key] == value:
# #            results.append(record) 

#     return jsonify(results)


# if __name__ == "__main__":
#     app.run()



