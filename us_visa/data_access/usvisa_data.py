import sys
from typing import Optional

import pandas as pd
import numpy as np

from us_visa.configuration.mongo_db_connection import MongoDBClient
from us_visa.constants import DATABASE_NAME
from us_visa.exception import USvisaException


class USvisaData:
    """
    This class exports MongoDB collections as pandas DataFrames.
    """

    def __init__(self):
        """
        Initialize MongoDB client.
        """
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise USvisaException(e, sys) from e

    def export_collection_as_dataframe(
        self,
        collection_name: str,
        database_name: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Export a MongoDB collection into a pandas DataFrame.
        """
        try:
            # Select database safely
            if database_name:
                db = self.mongo_client.client[database_name]
            else:
                db = self.mongo_client.database

            # Get collection
            collection = db[collection_name]

            # Fetch data
            data = list(collection.find())

            if not data:
                return pd.DataFrame()

            # Convert to DataFrame
            df = pd.DataFrame(data)

            # Drop MongoDB internal id field
            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            # Normalize missing values
            df.replace("na", np.nan, inplace=True)

            return df

        except Exception as e:
            raise USvisaException(e, sys) from e