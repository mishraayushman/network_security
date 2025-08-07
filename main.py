"""
This file is to test and trigger each and everything
"""

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logg
from networksecurity.components.data_validation import DataValidation
import sys
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

if __name__ =="__main__":
    try:
        Training_Pipeline_Config=TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(Training_Pipeline_Config)
        dataingestion = DataIngestion(data_ingestion_config)
        logg.info("initiate data_ingestion")
        data_ingestion_artifacts = dataingestion.initiate_data_ingestion()
        print(data_ingestion_artifacts)

        data_validation_config=DataValidationConfig(Training_Pipeline_Config)
        data_validation = DataValidation(data_ingestion_artifacts,data_validation_config)
        logg.info("initiate the data validation")
        data_validation_artifacts=data_validation.initiate_data_validation()
        logg.info("data Validation completed")
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)
