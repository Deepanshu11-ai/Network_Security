from networksecurity.entity.artifact_entity import ArtifactEntity,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from scipy.stats import ks_2samp
import pandas as pd
import os,sys
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.utils import read_yaml_file
class DataValidation:
    def __init__(self,data_ingestion_artifact:ArtifactEntity,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_config=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException (e,sys)