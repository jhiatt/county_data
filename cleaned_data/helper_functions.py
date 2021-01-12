import json
import pandas as pd

def jsonInserter(geojson,data,columnName,fileame):
    # this function takes our existing grouped_geojson file and adds our data to it and saves it as a new file
    # data needs to be formated as a dataframe with a 'fips' column and a second column holding the critical values, and a third column for period called 'Period'

    # loop through states
    for st in geojson['features']:

        # loop through counties for that state
        for ct in st['properties']['counties']:

            # find the data in the csv for the county's matching fips
            values = data[data['fips']==ct['id']][[columnName,'Period']]
            
            ct['value'] = values.to_json(orient='split')

            # print(values)
            # ct['value']
            # .to_json()

            # need to modify county data, should be a series of arrays? ordered list? to account for multiple time periods.
                # will this work now???
    
    with open(fileame, 'w') as outfile:
        json.dump(geojson, outfile)

# testing the function
with open('cleaned_data/grouped_geojson.json') as json_file:
    gj = json.load(json_file)

df_csv = pd.read_csv('cleaned_data/unemployment.csv',dtype=str)
data = df_csv[['fips','Unemployment_rate','Period']]

jsonInserter(gj, data,'Unemployment_rate', 'test.json')

