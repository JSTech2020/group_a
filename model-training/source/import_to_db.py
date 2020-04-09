import sys
import pandas as pd
from pymongo import MongoClient


# function to import csv data into db collection
def import_to_db(db_uri, db_name, collection_name, csv_file, separator=';', com_engine='python'):
    # read csv file as pandas data frame
    df = pd.read_csv(csv_file, sep=separator, engine=com_engine)

    # filter to include only data with is_published is true
    if collection_name == 'stories':
        df = df[(df['is_published'] == True)]

    doc_count = 0

    # exception handling for database operation
    try:
        # init mongodb client
        client = MongoClient(db_uri)
        db = client[db_name]

        # check if collection already exists, if so, remove(drop) the collection for now
        if collection_name in db.list_collection_names():
            collection = db[collection_name]
            if collection.estimated_document_count() != 0:
                print('Dropping the old collection (' + collection_name + ') ...')
                collection.drop()

                # TODO: Write an update code instead of drop and create new db.
                # However,recreating table is fast, maybe faster than reading each row and adding/updating

        # convert pandas data frame into dictionary for db insert
        collection = db[collection_name]
        data_dict = df.to_dict('records')

        # bulk insert collection data
        collection.insert_many(data_dict)
        doc_count = collection.estimated_document_count()
        print('Database import successful')
    except:  # TODO: maybe be specific about the exceptions that can occur
        print('Unexpected error:', sys.exc_info()[0])
        return False
        # raise
    return doc_count


# config for the import
uri = 'mongodb://localhost:27017/'
database = 'zs_database'
table = 'stories'
filename = '../resources/files/zs.csv'

# call the import function
doc_count = import_to_db(uri, database, table, filename)

if doc_count is not False:
    print(str(doc_count) + " documents were imported into stories collection")

