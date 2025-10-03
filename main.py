from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
if __name__=="__main__":
    try:
        logging.info("Starting the data ingestion component")
        training_pipeline_config = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(dataingestionconfig)
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info(f"Data ingestion artifact:{dataingestionartifact}")
        print(dataingestionartifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)