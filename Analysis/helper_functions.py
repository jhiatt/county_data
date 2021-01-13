import json
import pandas as pd

def jsonInserter(geojson,data,columnName,fileame):
    # this function takes our existing grouped_geojson file and adds our data to it and saves it as a new file
    # data needs to be formated as a dataframe with a 'fips' column and a second column holding the critical values, and a third column for period called 'Period'
    # in data, all counties need to have the same number of periods.  If there is no data we should specify.

    # set this variable to an impossible number so we can catch it if it is the first run and hadle differently
    prevValues = -9999

    # loop through states
    for st in geojson['features']:

        # loop through counties for that state
        for ct in st['properties']['counties']:

            # find the data in the csv for the county's matching fips
            values = data[data['fips']==ct['id']][[columnName,'Period']]

            # save to geojson object
            ct['value'] = values.to_json(orient='split', index=False)

            # check that the length of values is the same length as the values array previous
            # this should ensure that all counties have the same number of months in their data.
            # if data is completely missing this is easily ignored on the front end so we are not worried.
            if prevValues != -9999:
                if prevValues != len(values.Period) and not values.empty:
                    print(ct)
                    print(values)
                    raise Exception('some array does not have the same number of dates')
            
            # if data is completely missing we will effectively skip that county.
            if len(values.Period) != 0:
                prevValues = len(values.Period)
    

    with open(fileame, 'w') as outfile:
        json.dump(geojson, outfile)

# testing the function
# with open('cleaned_data/grouped_geojson.json') as json_file:
#     gj = json.load(json_file)

# df_csv = pd.read_csv('cleaned_data/unemployment.csv',dtype=str)
# data = df_csv[['fips','Unemployment_rate','Period']]

# jsonInserter(gj, data,'Unemployment_rate', 'cleaned_data/test.json')