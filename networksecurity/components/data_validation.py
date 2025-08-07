from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logg
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH 
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
from networksecurity.entity.artifact_entity import DataValidationArtifact
from scipy.stats import ks_2samp
import pandas as pd
import os,sys

class DataValidation:
    def __init__(self,data_ingestion_artifacts:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifacts
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path) ->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys) 
    
    def Validate_no_cols(self,dataframe:pd.DataFrame)->bool:
        try:
            no_cols = len(self._schema_config)
            logg.info(f"Required number of cols:{no_cols}")
            logg.info(f"Data frame has cols:{len(dataframe.columns)}")
            if len(dataframe.columns) == no_cols:
                return True
            else:
                return False
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def validate_cols_numeric(self,dataframe:pd.DataFrame)->bool:
        try:
            expected_cols = self._schema_config["numerical_columns"]
            missing_num_cols = [c for c in expected_cols if c not in dataframe.columns ]
            if missing_num_cols:
                logg.warning(f"Missing numerical columns: {missing_num_cols}")
                return False
            return True
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def detect_data_drift(self,base_df,current_df,threshold=0.5)->bool:
        try:
            status =True
            report={}
            for col in base_df.columns:
                d1=base_df[col]
                d2 =current_df[col]
                is_same_dist = ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found =False
                else:
                    is_found = True
                    status=False
                report.update({
                    col:{
                        "pvalue":float(is_same_dist.pvalue),
                        "drift_status":is_found
                    }
                })
            drift_report_file_path = self.data_validation_config.drift_data_report_file_path
            
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    
    
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            #reading the data
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            # validate number of cols
            status = self.Validate_no_cols(dataframe=train_df)
            if not status:
                error_message=f"Train dataframe does not contains all columns. \n"
            status2 = self.Validate_no_cols(dataframe=test_df)
            if not status2:
                error_message=f"Test dataframe does not contains all columns.\n"
            
            status_num_train = self.validate_cols_numeric(train_df)
            if not status_num_train:
                error_message = f"Train dataframe are missing numeric cols.\n"
            status_num_test = self.validate_cols_numeric(test_df)
            if not status_num_test:
                error_message = f"Test dataframe are missing with numeric cols. \n"

            status3 = self.detect_data_drift(base_df=train_df,current_df=test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_path)
            os.makedirs(dir_path,exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_path,index=False,header=True)
            test_df.to_csv(self.data_validation_config.valid_test_path,index=False,header=True)

            data_validation_artifacts = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_data_report_file_path=self.data_validation_config.drift_data_report_file_path
            )

            return data_validation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
