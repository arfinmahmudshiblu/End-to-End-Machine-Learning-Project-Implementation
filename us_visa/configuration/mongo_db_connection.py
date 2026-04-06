import os
import sys
from typing import Optional

import pymongo
import certifi

from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.constants import DATABASE_NAME, MONGODB_URL_KEY

# CA certificate for secure TLS connection
ca = certifi.where()


class MongoDBClient:
    """
    MongoDB Client Handler

    Description:
        Establishes and manages a MongoDB connection.

    Attributes:
        client (MongoClient): Shared MongoDB client instance
        database (Database): Selected database instance
    """

    client: Optional[pymongo.MongoClient] = None

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        try:
            # Initialize client only once (Singleton pattern)
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)

                if not mongo_db_url:
                    raise ValueError(
                        f"Environment variable '{MONGODB_URL_KEY}' is not set."
                    )

                MongoDBClient.client = pymongo.MongoClient(
                    mongo_db_url,
                    tls=True,
                    tlsCAFile=ca,
                    serverSelectionTimeoutMS=5000  # fail fast if cannot connect
                )

                # Test connection
                MongoDBClient.client.admin.command("ping")
                logging.info("MongoDB connection established successfully.")

            # Assign shared client
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name

        except Exception as e:
            logging.error("Failed to connect to MongoDB.")
            raise USvisaException(e, sys) from e

    def get_collection(self, collection_name: str):
        """
        Get a collection from the database
        """
        try:
            return self.database[collection_name]
        except Exception as e:
            raise USvisaException(e, sys) from e