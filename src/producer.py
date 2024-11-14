import pandas as pd
from kafka import KafkaProducer
from json import dumps
import os

# Kafka Configuration
KAFKA_TOPIC = 'happinessPredictions'
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']

# Load the cleaned dataset
dataset_path = os.path.join(os.path.dirname(__file__), "../clear_data/happiness_data.csv")
df = pd.read_csv(dataset_path)

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: dumps(v).encode('utf-8')
)

# Send all rows to Kafka without intervals
for index, row in df.iterrows():
    message = row.to_dict()
    producer.send(KAFKA_TOPIC, value=message)
    print(f"Sent: {message}")

producer.flush()
producer.close()
print("All data sent to Kafka successfully.")