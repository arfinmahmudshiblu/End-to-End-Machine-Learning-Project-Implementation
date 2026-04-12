import sys
from typing import Optional
import logging
from us_visa.components.data_validation import DataValidation
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.components.data_ingestion import DataIngestion
# from us_visa.components.data_validation import DataValidation 


from us_visa.entity.config_entity import (DataIngestionConfig,
                                           DataValidationConfig)
                                                                                   

from us_visa.entity.artifact_entity import (DataIngestionArtifact,
                                            DataValidationArtifact)
                               


class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
            

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        This method of TrainPipeline class is responsible for starting data ingestion component
        """
        try:
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Getting the data from mongodb")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train_set and test_set from mongodb")
            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )
            return data_ingestion_artifact
        except Exception as e:
            raise USvisaException(e, sys) from e
        

    
    def start_data_validation(
        self,data_ingestion_artifact: DataIngestionArtifact
        ) ->DataValidationArtifact:
        """
        This method of TrainPipeline class starts the data validation component.
        """
        logging.info("Entered start_data_validation method of TrainPipeline class")

        try:
            # Initialize DataValidation component
            data_validation = DataValidation(
            data_ingestion_artifact=data_ingestion_artifact,
            data_validation_config=self.data_validation_config
            )

            # Run validation
            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Data validation completed successfully")

            logging.info("Exited start_data_validation method of TrainPipeline class")

            return data_validation_artifact

        except Exception as e:
            logging.error("Error occurred in start_data_validation method")
            raise USvisaException(e, sys) from e

    
    def run_pipeline(self, ) -> None:
        """
        This method of TrainPipeline class is responsible for running complete pipeline
        """
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        
        except Exception as e:
            raise USvisaException(e, sys)    