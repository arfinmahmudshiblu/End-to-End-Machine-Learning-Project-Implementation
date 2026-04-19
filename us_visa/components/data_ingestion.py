# import os
# import sys

# from pandas import DataFrame
# from sklearn.model_selection import train_test_split

# from us_visa.entity.config_entity import DataIngestionConfig
# from us_visa.entity.artifact_entity import DataIngestionArtifact
# from us_visa.exception import USvisaException
# from us_visa.logger import logging
# from us_visa.data_access.usvisa_data import USvisaData


# class DataIngestion:
#     def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
#         """
#         :param data_ingestion_config: configuration for data ingestion
#         """
#         try:
#             self.data_ingestion_config = data_ingestion_config
#         except Exception as e:
#             raise USvisaException(e, sys) from e

#     def export_data_into_feature_store(self) -> DataFrame:
#         """
#         Export data from MongoDB to CSV file
#         """
#         try:
#             logging.info("Exporting data from MongoDB")

#             usvisa_data = USvisaData()

#             dataframe = usvisa_data.export_collection_as_dataframe(
#                 collection_name=self.data_ingestion_config.collection_name
#             )

#             logging.info(f"Shape of dataframe: {dataframe.shape}")

#             if dataframe.empty:
#                 raise Exception("No data found in MongoDB collection")

#             feature_store_file_path = self.data_ingestion_config.feature_store_file_path
#             dir_path = os.path.dirname(feature_store_file_path)

#             os.makedirs(dir_path, exist_ok=True)

#             logging.info(f"Saving data to: {feature_store_file_path}")

#             dataframe.to_csv(feature_store_file_path, index=False, header=True)

#             # ✅ Close connection AFTER data is fetched
#             usvisa_data.close_connection()

#             return dataframe

#         except Exception as e:
#             raise USvisaException(e, sys) from e

#     def split_data_as_train_test(self, dataframe: DataFrame) -> None:
#         """
#         Split dataframe into train and test sets
#         """
#         logging.info("Entered split_data_as_train_test method")

#         try:
#             train_set, test_set = train_test_split(
#                 dataframe,
#                 test_size=self.data_ingestion_config.train_test_split_ratio,
#                 random_state=42  # ✅ reproducibility
#             )

#             logging.info("Performed train-test split")

#             dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
#             os.makedirs(dir_path, exist_ok=True)

#             logging.info("Saving train and test datasets")

#             train_set.to_csv(
#                 self.data_ingestion_config.training_file_path,
#                 index=False,
#                 header=True
#             )

#             test_set.to_csv(
#                 self.data_ingestion_config.testing_file_path,
#                 index=False,
#                 header=True
#             )

#             logging.info("Train-test files saved successfully")

#         except Exception as e:
#             raise USvisaException(e, sys) from e

#     def initiate_data_ingestion(self) -> DataIngestionArtifact:
#         """
#         Run full data ingestion pipeline
#         """
#         logging.info("Starting data ingestion process")

#         try:
#             dataframe = self.export_data_into_feature_store()

#             logging.info("Data fetched from MongoDB")

#             self.split_data_as_train_test(dataframe)

#             logging.info("Train-test split completed")

#             data_ingestion_artifact = DataIngestionArtifact(
#                 trained_file_path=self.data_ingestion_config.training_file_path,
#                 test_file_path=self.data_ingestion_config.testing_file_path
#             )

#             logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

#             return data_ingestion_artifact

#         except Exception as e:
#             raise USvisaException(e, sys) from e