import sys
import json
import pandas as pd
import os


from evidently import Report
from evidently.metrics import *
from evidently.presets import *
from evidently.presets import DataDriftPreset
from evidently.presets import DataSummaryPreset

from pandas import DataFrame

from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.utils.main_utils import read_yaml_file, write_yaml_file
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.constants import SCHEMA_FILE_PATH


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

        except Exception as e:
            raise USvisaException(e, sys)

    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        try:
            expected_cols = self._schema_config.get("columns", [])
            status = len(dataframe.columns) == len(expected_cols)

            logging.info(f"Column count validation: {status}")
            return status

        except Exception as e:
            raise USvisaException(e, sys)

    def is_column_exist(self, df: DataFrame) -> bool:
        try:
            dataframe_columns = df.columns

            missing_numerical = [
                col for col in self._schema_config.get("numerical_columns", [])
                if col not in dataframe_columns
            ]

            missing_categorical = [
                col for col in self._schema_config.get("categorical_columns", [])
                if col not in dataframe_columns
            ]

            if missing_numerical:
                logging.info(f"Missing numerical columns: {missing_numerical}")

            if missing_categorical:
                logging.info(f"Missing categorical columns: {missing_categorical}")

            return not (missing_numerical or missing_categorical)

        except Exception as e:
            raise USvisaException(e, sys) from e

    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise USvisaException(e, sys)

    def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame) -> bool:
        try:
            if reference_df.empty or current_df.empty:
                raise ValueError("Reference or current dataframe is empty.")

            report = Report(metrics=[DataDriftPreset()])

            report.run(
                reference_data=reference_df,
                current_data=current_df
            )

            report_dict = report.as_dict()

            write_yaml_file(
                file_path=self.data_validation_config.drift_report_file_path,
                content=report_dict
            )

            metrics = report_dict.get("metrics", [{}])[0].get("result", {})

            n_features = metrics.get("number_of_columns", 0)
            n_drifted = metrics.get("number_of_drifted_columns", 0)
            drift_status = metrics.get("dataset_drift", False)

            logging.info(
                f"Drift status: {drift_status}, "
                f"{n_drifted}/{n_features} drifted features"
            )

            return drift_status

        except Exception as e:
            logging.error(f"Error in drift detection: {str(e)}")
            raise USvisaException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("Starting data validation")

            train_df = DataValidation.read_data(self.data_ingestion_artifact.trained_file_path)
            test_df = DataValidation.read_data(self.data_ingestion_artifact.test_file_path)

            validation_error_msg = ""

            if not self.validate_number_of_columns(train_df):
                validation_error_msg += "Training column mismatch. "

            if not self.validate_number_of_columns(test_df):
                validation_error_msg += "Test column mismatch. "

            if not self.is_column_exist(train_df):
                validation_error_msg += "Missing training columns. "

            if not self.is_column_exist(test_df):
                validation_error_msg += "Missing test columns. "

            validation_status = len(validation_error_msg.strip()) == 0

            drift_status = False

            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                validation_error_msg = (
                    "Drift detected" if drift_status else "No drift detected"
                )
            else:
                logging.info(f"Validation errors: {validation_error_msg}")

            artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data validation artifact: {artifact}")
            return artifact

        except Exception as e:
            raise USvisaException(e, sys) from e