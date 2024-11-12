from kafka import KafkaConsumer
from sqlalchemy import create_engine, Column, Float, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import json

# Cargar variables de entorno desde .env
load_dotenv()
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/{os.getenv('POSTGRES_DB')}"

# Configuración de la base de datos con SQLAlchemy
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Definir la tabla de predicciones
class HappinessPrediction(Base):
    __tablename__ = 'happiness_predictions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    country = Column(String)
    region = Column(String)
    gdp_per_capita = Column(Float)
    healthy_life_expectancy = Column(Float)
    freedom = Column(Float)
    perceptions_of_corruption = Column(Float)
    generosity = Column(Float)
    predicted_happiness_score = Column(Float)

# Crear la tabla en la base de datos si no existe
Base.metadata.create_all(engine)

# Configurar el consumidor de Kafka
consumer = KafkaConsumer(
    'happiness_predictions',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Consumir mensajes de Kafka y almacenarlos en PostgreSQL
for message in consumer:
    data = message.value
    features = data['features']
    predicted_score = data['predicted_happiness_score']

    # Crear instancia de predicción
    prediction = HappinessPrediction(
        country=features['country'],
        region=features['region'],
        gdp_per_capita=features['gdp_per_capita'],
        healthy_life_expectancy=features['healthy_life_expectancy'],
        freedom=features['freedom'],
        perceptions_of_corruption=features['perceptions_of_corruption'],
        generosity=features['generosity'],
        predicted_happiness_score=predicted_score
    )
    
    # Agregar a la base de datos
    session.add(prediction)
    session.commit()
    print("Predicción almacenada en PostgreSQL:", prediction)

session.close()