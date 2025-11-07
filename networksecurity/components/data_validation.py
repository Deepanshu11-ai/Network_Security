from networksecurity.entity.artifact_entity import ArtifactEntity,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logger
from scipy.stats import ks_2samp
import pandas as pd
import os,sys
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.utils import read_yaml_file,write_yaml_file
class DataValidation:
    def __init__(self,data_ingestion_artifact:ArtifactEntity,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException (e,sys)
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def validat_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self._schema_config["columns"])
            logger.info(f"required number of columns :{number_of_columns}")
            logger.info(f"dataframe has columns :{len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:
                return True
            return False
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            logger.info("starting data validation")
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)

            status=self.validat_number_of_columns(dataframe=train_dataframe)
            if not status:
                raise NetworkSecurityException("number of columns are not matching",sys)
            status=self.validat_number_of_columns(dataframe=test_dataframe)
            if not status:
                raise NetworkSecurityException("number of columns are not matching",sys)
            
            #data drift
            status=self.detect_data_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)

            data_validation_artifact=DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_test_file_path=None,
                invalid_train_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
          
    def detect_data_drift(self,base_df, current_df=None, threshold=0.05)->bool:
        try:
            status=True
            report={}
            # If current_df is not provided, compare base_df with itself (no drift)
            if current_df is None:
                current_df = base_df

            for column in base_df.columns:
                d1=base_df[column].dropna()
                d2=current_df[column].dropna() if column in current_df.columns else d1
                result = ks_2samp(d1, d2)
                p_value = float(result.pvalue)
                # if p_value is less than threshold, drift is detected for that column
                column_has_drift = p_value < threshold
                if column_has_drift:
                    status = False
                report.update({column:{"p_value":p_value,"drift_status":column_has_drift}})
            drift_report_file_path=self.data_validation_config.drift_report_file_path

            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)

            return status
            
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e