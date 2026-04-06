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
conda create -n webapp python=3.12 -y
```

```bash
conda activate webapp
```

```bash
pip install -r requirements.txt
```
# Export the environment variable

```bash
export MONGODB_URL="mongodb+srv://arfin:arfin@cluster0.2wvohg6.mongodb.net/?appName=Cluster0"
```

# Components (Must be used this sequence)
1. data_ingestion.py
2. data_validation.py
3. data_transformation.py
4. model_trainer.py
5. model_evaluation.py
6. model_pusher.py
