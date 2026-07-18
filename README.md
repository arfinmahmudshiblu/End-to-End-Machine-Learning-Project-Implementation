# End-to-End-Machine-Learning-Project-Implementation

# Tool you have to install:-

1. Anaconda: https://www.anaconda.com/
2. Vs code: https://code.visualstudio.com/download
3. Git: https://git-scm.com/

# Data link:
Kaggle: https://www.kaggle.com/datasets/moro23/easyvisa-dataset

# Database used:
MongoDB: https://account.mongodb.com/account/login

# Workflow
1. constant
2. config_entity
3. artifact_entity
4. component
5. pipeline
6. app.py / demo.py

# How to run?

```bash
git clone https://github.com/arfinmahmudshiblu/End-to-End-Machine-Learning-Project-Implementation.git
```

```bash
conda create -n cnncls python=3.8 -y
```

```bash
conda activate cnncls
```

```bash
pip install -r requirements.txt
```

# Export the environment variable

```bash
export MONGODB_URL="mongodb+srv://arfin:arfin@cluster0.s0ljlbs.mongodb.net/?appName=Cluster0"
```

# Components (Must be used this sequence)
1. data_ingestion.py
2. data_validation.py
3. data_transformation.py
4. model_trainer.py
5. model_evaluation.py
6. model_pusher.py


# First Work Flow(Data Ingestion)
1. constant
2. config_entity.py
3. artifact_entity.py
4. mongodb_connection.py
5. usvisa_data.py
6. component_data_ingestion.py
7. training_pipeline.py
8. demo.py

# Second Work Flow(Data Validation)
1. constant
2. config_schema.yaml
3. config_entity.py
4. artifact_entity.py
5. component_data_validation.py
6. training_pipeline.py
7. demo.py

# Third Work Flow(Data Transformation)
1. constant
2. config_entity.py
3. artifact_entity.py
4. component_data_transformation.py
5. us_visa_entity_estimator.py
6. training_pipeline.py
7. demo.py

# Forth Work Flow(Model_Trainer)
1. constant
2. config_entity.py
3. artifact_entity.py
4. component_data_transformation.py
5. us_visa_entity_estimator.py
6. model.yaml
7. training_pipeline.py
8. demo.py


## Project Structure

```text
USVISAProject/
│
├── artifacts/
│   ├── feature_store/
│   └── ingested/
│
├── config/
│   ├── model.yaml
│   └── schema.yaml
│
├── notebooks/
│    ├── EDA_US_visa.ipynb
│    ├── Feature_Engineering_&_Model_Training.ipynb
│    ├── evidently_data_drift_detection.ipynb
│    ├── Visadataset.csv
│    └── mongoDB_test.ipynb
│
├── us_visa/
│   ├── __init__.py
│   │
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   ├── model_evaluation.py
│   │   └── model_pusher.py
│   │
│   ├── configuration/
│   │   └── mongo_db_connection.py
│   │
│   ├── constants/
│   │   └── __init__.py
│   │
│   ├── data_access/
│   │   ├── __init__.py
│   │   └── usvisa_data.py
│   │
│   ├── entity/
│   │   ├── __init__.py
│   │   ├── config_entity.py
│   │   └── artifact_entity.py
│   │
│   ├── pipeline/
│   │   ├── training_pipeline.py
│   │   └── prediction_pipeline.py
│   │   
│   │
│   ├── utils/
│   │   ├── __init__.py   
│   │   └── main_utils.py
│   │
│   ├── exception.py
│   │   └── __init__.py
│   └── logger.py
│       └── __init__.py
│
│
├── templates/
│   └── index.html
│
├── .gitignore
├── app.py
├── demo.py
├── README.md
├── requirements.txt
├── setup.py
├── templates.py
└── test.py
```