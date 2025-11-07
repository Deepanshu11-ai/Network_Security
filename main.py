from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_transformation import DataTransformation,DataTransformationConfig
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataValidationConfig
import sys
if __name__=="__main__":
    try:
        logger.info("Starting the data ingestion component")
        training_pipeline_config = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(dataingestionconfig)
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logger.info(f"Data ingestion artifact:{dataingestionartifact}")
        print(dataingestionartifact)

        # Prepare data validation config and run validation
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(dataingestionartifact, data_validation_config)
        logger.info("Starting data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logger.info(f"Data validation artifact:{data_validation_artifact}")
        data_transformation_config=DataTransformationConfig(training_pipeline_config)
        data_transforamtion=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transforamtion.initiate_data_transformation()
        print(data_transformation_artifact)
        logger.info(f"Data Transformation artifact:{data_transformation_artifact}")
    except Exception as e:
        raise NetworkSecurityException(e, sys)