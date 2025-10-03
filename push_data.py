import os
import sys
import json
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()
import pandas as pd
import pymongo
import logging

from networksecurity.exception.exception import NetworkSecurityException

class NetworkDataExtract():
    def __init__(self):
        try:
            self.logger = logging.getLogger("NetworkDataExtract")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, file_path):
        try:
            path = Path(file_path)
            data = pd.read_csv(path)
            data.reset_index(drop=True, inplace=True)
            # produce a list of record dicts suitable for insert_many
            records = json.loads(data.to_json(orient="records"))
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def push_data_to_mongo(self, records, database, collection):
        try:
            if not MONGO_DB_URL:
                raise ValueError("MONGO_DB_URL is not set in environment")
            client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            db = client[database]
            coll = db[collection]
            result = coll.insert_many(records)
            return len(result.inserted_ids)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = r"Network_Data\phisingData.csv"
    DATABASE_NAME = "NetworkSecurity"
    COLLECTION_NAME = "PhishingData"

    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_converter(FILE_PATH)
    no_of_records = networkobj.push_data_to_mongo(records, DATABASE_NAME, COLLECTION_NAME)
    print(f"Total number of records inserted in mongo db is : {no_of_records}")