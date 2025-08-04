"""
This file is to test and trigger each and everything
"""

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logg
import sys
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

if __name__ =="__main__":
    try:
        TrainingPipelineConfig=TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(TrainingPipelineConfig)
        dataingestion = DataIngestion(data_ingestion_config)
        logg.info("initiate data_ingestion")
        data_ingestion_artifacts = dataingestion.initiate_data_ingestion()
        print(data_ingestion_artifacts)
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)
