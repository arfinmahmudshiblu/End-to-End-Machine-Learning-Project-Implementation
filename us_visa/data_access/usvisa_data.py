import sys
from typing import Optional

import pandas as pd
import numpy as np

from us_visa.configuration.mongo_db_connection import MongoDBClient
from us_visa.constants import DATABASE_NAME
from us_visa.exception import USvisaException


class USvisaData:
    """
    This class helps to export entire MongoDB collections as pandas DataFrames.
    """

    def __init__(self):
        """
        Initialize the MongoDB client.
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise USvisaException(e, sys) from e

    def export_collection_as_dataframe(
        self, collection_name: str, database_name: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Export an entire MongoDB collection as a pandas DataFrame.

        Args:
            collection_name (str): Name of the MongoDB collection.
            database_name (Optional[str]): If provided, overrides the default database.

        Returns:
            pd.DataFrame: DataFrame containing the collection data.
        """
        try:
            # Select the database
            db = self.mongo_client.database if database_name is None else self.mongo_client.client[database_name]

            # Get the collection
            collection = db[collection_name]

            # Fetch all documents
            data = list(collection.find())

            if not data:
                return pd.DataFrame()  # Return empty DataFrame if collection is empty

            # Convert to DataFrame
            df = pd.DataFrame(data)

            # Drop MongoDB '_id' field if exists
            if "_id" in df.columns:
                df = df.drop(columns=["_id"])

            # Replace string "na" with np.nan
            df.replace("na", np.nan, inplace=True)

            return df

        except Exception as e:
            raise USvisaException(e, sys) from e