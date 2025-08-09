import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logg

from networksecurity.constants.training_pipeline import TARGET_COLUMN
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import(
    DataTranformationArtifacts,
    DataValidationArtifact
)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import save_numpy_array,save_obj



class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifacts:DataValidationArtifact = data_validation_artifact
            self.data_transformation_config:DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    @staticmethod
    def read_data(file_path) ->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def get_data_transformed_object(cls) -> Pipeline:
        logg.info("Entered Data transformation class")
        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logg.info(
                f"Initialize KNNimputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"

            )
            processor:Pipeline = Pipeline([("imputer",imputer)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self) -> DataTranformationArtifacts:
        logg.info("Entered initiate_data_transformation method ")
        try:
            logg.info("Starting data Transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifacts.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifacts.valid_test_file_path)

            #train df
            input_features_train_df =train_df.drop(TARGET_COLUMN,axis=1)
            target_feature_train_df =train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            #test df
            input_features_test_df =test_df.drop(TARGET_COLUMN,axis=1)
            target_feature_test_df =test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            preprocessor = self.get_data_transformed_object()
            preprocessor_obj = preprocessor.fit(input_features_train_df)
            transformed_train_data = preprocessor_obj.transform(input_features_train_df)
            transformed_test_data = preprocessor_obj.transform(input_features_test_df)
            
            train_arr = np.c_[transformed_train_data,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_test_data,np.array(transformed_test_data)]

            #save numpy array data
            save_numpy_array(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array(self.data_transformation_config.transformed_test_file_path,array=test_arr)
            save_obj(self.data_transformation_config.transformed_object_file_path,preprocessor_obj)

            #prepareing artifacts
            data_transformation_artifacts = DataTranformationArtifacts(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path =self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_train_file_path
            )
            return data_transformation_artifacts
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)