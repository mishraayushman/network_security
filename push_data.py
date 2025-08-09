import os 
import sys
import json
from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

print(MONGO_DB_URL)

import certifi 
ca = certifi.where()# this retrives a path ,bundle of CA certificates provideed by certifi and store it in variable ca.


"""
## Certifi:

- it is package that provide set of Root Certificates
When you make secure HTTPS requests (e.g., using requests, urllib3, etc.), 
your Python program needs a list of trusted Certificate Authorities to verify the server’s certificate.
Without this, your connection could be insecure or fail.

"""

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logg

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def csv_to_json(self,file_path):
        try:
            data = pd.read_csv(file_path,header=0)
            data.reset_index(drop=True,inplace=True)
            record =list(json.loads(data.T.to_json()).values())
            return record
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection =collection
            self.records = records

            self.mongoclient =pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongoclient[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)


if __name__ == "__main__":
    FILE_PATH ="F:\\Network_Security\\netwok_data\\phisingData.csv"
    DATABASE = "Ayushman"
    collection = "NetworkData"
    networkobj = NetworkDataExtract()
    records =networkobj.csv_to_json(FILE_PATH)
    print(records)
    num_of_records =networkobj.insert_data_mongodb(records,DATABASE,collection)
    print(num_of_records)
