# ...existing code...
import os
import sys
import json
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
import logging

from typing import List

from sklearn.model_selection import train_test_split

from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.logging.logger import logger

from networksecurity.entity.config_entity import DataIngestionConfig

from networksecurity.entity.artifact_entity import ArtifactEntity

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config

            # read DB/collection names from config (fallback to sensible defaults)
            self.database_name = getattr(data_ingestion_config, "database_name", "NetworkSecurity")

            self.collection_name = getattr(data_ingestion_config, "collection_name", "PhishingData")

            # initialize mongo client if URL present
            if MONGO_DB_URL:
                self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            else:
                self.mongo_client = None

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self) -> pd.DataFrame:

        df = pd.DataFrame()
        try:
            if not self.mongo_client:
                raise Exception("Mongo client not initialized. Set MONGO_DB_URL in environment.")

            cursor = self.mongo_client[self.database_name][self.collection_name].find()
            records = list(cursor)
            if not records:
                logger.info("No records found in collection %s.%s", self.database_name, self.collection_name)
                return df

            df = pd.DataFrame(records)

            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            return df

        except Exception as e:
            # Log the MongoDB error and attempt to fallback to a local CSV file if available.
            logger.error("Failed to export collection from MongoDB: %s", str(e))

            local_csv = os.path.join(os.getcwd(), "Network_Data", "phisingData.csv")
            if os.path.exists(local_csv):
                try:
                    logger.info("Falling back to local CSV at %s", local_csv)
                    df = pd.read_csv(local_csv)
                    return df
                except Exception as read_e:
                    logger.error("Failed to read fallback CSV: %s", str(read_e))

            # If fallback not available or failed, re-raise as project exception.
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            dir_path = os.path.dirname(feature_store_file_path)

            os.makedirs(dir_path, exist_ok=True)

            df.to_csv(feature_store_file_path, index=False, header=True)

            return df
        except Exception as e:

            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, df: pd.DataFrame) -> None:

        try:
            train_set, test_set = train_test_split(

                df,

                test_size=self.data_ingestion_config.train_test_split_ratio,

                random_state=42
            )

            logging.info("Performed train test split")

            dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)

            os.makedirs(dir_path, exist_ok=True)

            logging.info("Exporting train and test file path")

            train_set.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)

            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()

            dataframe = self.export_data_into_feature_store(dataframe)

            self.split_data_as_train_test(dataframe)

            dataingestionartifact = ArtifactEntity(
                trained_file_path=self.data_ingestion_config.train_file_path,

                test_file_path=self.data_ingestion_config.test_file_path
            )

            return dataingestionartifact

        except Exception as e:

            raise NetworkSecurityException(e, sys)
# ...existing code...