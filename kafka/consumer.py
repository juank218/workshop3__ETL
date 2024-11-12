from kafka import KafkaConsumer
import pickle
import pandas as pd
from json import loads
from sqlalchemy import create_engine, Column, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
db_connection_url = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(db_connection_url)
Base = declarative_base()


class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    health = Column(Float)
    social_support = Column(Float)
    economy = Column(Float)
    corruption_perception = Column(Float)
    freedom = Column(Float)
    happiness_score = Column(Float)


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

def kafka_consumer():

    with open("../model/gb_model.pkl", "rb") as f:
        model = pickle.load(f)

    consumer = KafkaConsumer(
        'happiness_topic',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda m: loads(m.decode('utf-8'))
    )

    for message in consumer:
        features = message.value  
        features_df = pd.DataFrame([features])  

        prediction = model.predict(features_df)[0]  
        features["happiness_score"] = prediction  


        new_prediction = Prediction(
            year=features["year"],
            health=features["health"],
            social_support=features["social_support"],
            economy=features["economy"],
            corruption_perception=features["corruption_perception"],
            freedom=features["freedom"],
            happiness_score=features["happiness_score"]
        )

        session.add(new_prediction)
        session.commit()
        print(f"Predicted happiness score for year {features['year']}: {prediction}")

    session.close()
