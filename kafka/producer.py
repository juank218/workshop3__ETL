from kafka import KafkaProducer
import pandas as pd
from json import dumps

def kafka_producer():
    data = pd.read_csv("../clear_data/happiness_data.csv")
    features = data.drop(["happiness_score", "happiness_rank", "country"], axis=1)

    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda m: dumps(m).encode('utf-8')
    )


    for _, row in features.iterrows():
        message = row.to_dict() 
        producer.send('happiness_topic', value=message)
        print(f"Mensaje enviado: {message}")

    print("Todos los datos han sido enviados.")
    producer.flush()
    producer.close()
