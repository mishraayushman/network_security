from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logg

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL =os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_coonfig:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_coonfig
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_collection_to_dataframe(self):
        """
        Read Data from 
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongoClient = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongoClient[database_name][collection_name]

            df = pd.DataFrame(list(collection.find())) 
            if "_id" in df.columns.to_list():
                df = df.drop("_id",axis=1)
            df.replace({"na":np.nan},inplace=True)

            return df

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def train_test_split_data(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set =train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logg.info("Train_test_split done")
            dir_path =os.path.dirname(self.data_ingestion_config.training_data_path)
            os.makedirs(dir_path,exist_ok=True)

            logg.info("exporting train_set and test_set to csv")
            train_set.to_csv(self.data_ingestion_config.training_data_path,index=False,header=True)

            test_set.to_csv(self.data_ingestion_config.test_data_path,index=False,header=True)
            logg.info("Exported successfully")

        except Exception as e:
            raise NetworkSecurityException(e,sys)




    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_to_dataframe()
            dataframe1 = self.export_data_into_feature_store(dataframe)
            self.train_test_split_data(dataframe1)
            dataingestionartifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_data_path,
                test_file_path=self.data_ingestion_config.test_data_path

            )

            return dataingestionartifact
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)