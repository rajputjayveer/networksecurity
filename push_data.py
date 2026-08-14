import os
import sys
import json

from dotenv import load_dotenv
import numpy as np
import pandas as pd
import pymongo

load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")
# print(f"MONGO_DB_URI: {MONGO_DB_URI}")

import certifi
ca = certifi.where()

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def insert_data_to_mongodb(self, records, database , collection):
        try:
           self.database = database
           self.collection = collection
           self.records = records

           self.mongo_client = pymongo.MongoClient(MONGO_DB_URI)
           self.database = self.mongo_client[self.database]
           self.collection = self.database[self.collection]  

           self.collection.insert_many(self.records)
           return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "JayveerAI"
    COLLECTION = "NetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_converter(FILE_PATH)
    print(records)
    inserted_count = networkobj.insert_data_to_mongodb(records, DATABASE, COLLECTION)
    print(f"Inserted {inserted_count} records into MongoDB collection '{COLLECTION}' in database '{DATABASE}'.")

 

