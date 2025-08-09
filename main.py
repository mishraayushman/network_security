"""
This file is to test and trigger each and everything
"""

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logg
from networksecurity.components.data_validation import DataValidation
import sys
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
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
        print(data_validation_artifacts)
        logg.info("data Validation completed")

        data_transformation_config = DataTransformationConfig(Training_Pipeline_Config)
        data_tranformation =DataTransformation(data_validation_artifacts,data_transformation_config)
        logg.info("initiate the data transformation")
        data_transformation_artifacts = data_tranformation.initiate_data_transformation()
        print(data_transformation_artifacts)
        logg.info("Data transformation completed")

    except Exception as e:
        raise NetworkSecurityException(e,sys)
