# from us_visa.logger import logging

# logging.info("Logging setup complete.")



# from us_visa.logger import logging
# from us_visa.exception import USvisaException   
# import sys

# try:
#     r=3/0
# except Exception as e:
#     logging.info(e)
#     raise USvisaException(e, sys) 



# import os

# mongodburl=os.getenv("MONGODB_URL")
# print(mongodburl)

from us_visa.pipline.training_pipeline import TrainingPipeline


pipeline = TrainingPipeline()
pipeline.run_pipeline()