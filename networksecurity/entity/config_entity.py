from datetime import datetime
import os

from networksecurity.constant  import training_pipeline
print(training_pipeline.PIPELINE_NAME)

class TrainingPipelineConfig:
    def __init__(self):
        self.artifact_name = "artifact"
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        # place artifacts under the project's ARTIFACTS_DIR with a timestamped subfolder
        self.artifact_dir = os.path.join(training_pipeline.ARTIFACTS_DIR,
                                         self.artifact_name,
                                         timestamp)

"""class TrainingPipelineConfig:
    def __init__(self):
        self.artifact_name = "artifact"
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
-        self.artifact_dir = os.join(self.artifact_name, timestamp)
+        self.artifact_dir = os.path.join(self.artifact_name, timestamp)
# ...existing code..."""

class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        # directory for data ingestion inside the artifact folder
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path:str=os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILE_NAME
        )
        self.train_file_path:str=os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
        )
        self.test_file_path:str=os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
        )
        self.database_name:str=training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.collection_name:str=training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.train_test_split_ratio:float=training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION

class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir:str=os.path.join(training_pipeline.ARTIFACTS_DIR,training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )
