# workshop3__ETL 

# Context

The objective of this project is to analyze and preprocess five CSV files containing data on the happiness levels of various countries from 2015 to 2019. Each dataset includes columns such as country name, GDP, government trust, life expectancy, among others.

The workflow begins with the development of a Jupyter Notebook to perform Exploratory Data Analysis (EDA) on these CSV files, combining them into a single dataset. In a subsequent notebook, we will build and train a machine learning model to predict the happiness score of each country, following a thorough testing and validation phase.

Finally, the project utilizes Apache Kafka for data streaming. This involves two Python scripts: one that processes the data and sends it via Kafka under the topic "happinessPredictions," and a consumer script that retrieves the data, makes happiness predictions, and stores the results in a database.

# Workflow

The workflow consists of the following steps:
1. Load and preprocess the CSV files.
2. Conduct EDA to understand the data.
3. Train a machine learning model based on selected features.
4. Use Python scripts to stream data through Kafka.
5. Store the predictions in a database.

# Tools Used

- Python
- Jupyter Notebook
- CSV files
- PostgreSQL
- Kafka
- Docker
- Scikit-learn

# Steps to Reproduce the Process

Clone the repository:

```bash
git clone https://github.com/juank218/workshop3__ETL.git
```
Set up PostgreSQL and create an `.env` file to store database credentials:

# .env file example:

```bash
"LOCALHOST=" >> .env
"PORT="      >> .env
"DB_NAME="   >> .env
"DB_USER="   >> .env
"DB_PASS="   >> .env
```

# Create and activate a virtual environment with venv:

```bash
python3 -m venv venv
```

```bash
source env/bin/activate  
# On Windows use:
venv\Scripts\activate
```


# Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

# Start Docker:

```bash
docker-compose up -d
```

# Access the Kafka container's bash shell:

```bash
docker exec -it kafka-test bash
```

# Create a Kafka topic:

```bash
kafka-topics --bootstrap-server localhost:9092 --create --topic happinessPredictions
```

# Exit the bash shell:

```bash
exit
```

# Run the Python scripts on different terminals, in the following order:

```bash
cd src/
```

```bash
python consumer.py
```
```bash
cd src/
```

```bash
python ./kafka/process_data.py
```

# Testing

For a demonstration of this setup in action, you can view a sample test run video by following this [link to Google Drive](https://drive.google.com/file/d/12KPouRoPIdD_Nxhg-5y7rqMHzm4Mg6n4/view?usp=sharing).

# Final Output

Once all steps are complete, the database will contain the predicted happiness scores for each country, based on the processed data.
