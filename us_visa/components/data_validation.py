# import sys
# import json
# import pandas as pd
# import os


# from evidently import Report
# from evidently.metrics import *
# from evidently.presets import *
# from evidently.presets import DataDriftPreset
# from evidently.presets import DataSummaryPreset

# from pandas import DataFrame

# from us_visa.exception import USvisaException
# from us_visa.logger import logging
# from us_visa.utils.main_utils import read_yaml_file, write_yaml_file
# from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
# from us_visa.entity.config_entity import DataValidationConfig
# from us_visa.constants import SCHEMA_FILE_PATH


# class DataValidation:
#     def __init__(
#         self,
#         data_ingestion_artifact: DataIngestionArtifact,
#         data_validation_config: DataValidationConfig
#     ):
#         try:
#             self.data_ingestion_artifact = data_ingestion_artifact
#             self.data_validation_config = data_validation_config
#             self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)

#         except Exception as e:
#             raise USvisaException(e, sys)

#     def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
#         try:
#             expected_cols = self._schema_config.get("columns", [])
#             status = len(dataframe.columns) == len(expected_cols)

#             logging.info(f"Column count validation: {status}")
#             return status

#         except Exception as e:
#             raise USvisaException(e, sys)

#     def is_column_exist(self, df: DataFrame) -> bool:
#         try:
#             dataframe_columns = df.columns

#             missing_numerical = [
#                 col for col in self._schema_config.get("numerical_columns", [])
#                 if col not in dataframe_columns
#             ]

#             missing_categorical = [
#                 col for col in self._schema_config.get("categorical_columns", [])
#                 if col not in dataframe_columns
#             ]

#             if missing_numerical:
#                 logging.info(f"Missing numerical columns: {missing_numerical}")

#             if missing_categorical:
#                 logging.info(f"Missing categorical columns: {missing_categorical}")

#             return not (missing_numerical or missing_categorical)

#         except Exception as e:
#             raise USvisaException(e, sys) from e

#     @staticmethod
#     def read_data(file_path) -> DataFrame:
#         try:
#             return pd.read_csv(file_path)
#         except Exception as e:
#             raise USvisaException(e, sys)

#     def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame) -> bool:
#         try:
#             if reference_df.empty or current_df.empty:
#                 raise ValueError("Reference or current dataframe is empty.")

#             report = Report(metrics=[DataDriftPreset()])

#             report.run(
#                 reference_data=reference_df,
#                 current_data=current_df
#             )

#             # ✅ Save report directly
#             report.save_json(self.data_validation_config.drift_report_file_path)

#             # ✅ Load back as dict
#             report_dict = json.loads(report.json())

#             metrics = report_dict.get("metrics", [{}])[0].get("result", {})

#             drift_status = metrics.get("dataset_drift", False)

#             return drift_status

#         except Exception as e:
#             raise USvisaException(e, sys) from e