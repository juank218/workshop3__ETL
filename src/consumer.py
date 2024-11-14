import pandas as pd
from json import loads
import joblib
import os
import psycopg2
from kafka import KafkaConsumer
from dotenv import load_dotenv
from sqlalchemy import create_engine
import time

# Cargar variables de entorno
load_dotenv()

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASS")
db_host = os.getenv("LOCALHOST")
db_port = os.getenv("PORT")
db_database = os.getenv("DB_NAME")

# Crear conexión a PostgreSQL usando SQLAlchemy
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}")

# Cargar el modelo
model_file_path = '../model/gb_model.pkl'
model = joblib.load(model_file_path)

# Configuración del consumidor de Kafka
consumer = KafkaConsumer(
    'happinessPredictions',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='happiness_group',
    value_deserializer=lambda m: loads(m.decode('utf-8')),
    bootstrap_servers=['localhost:9092'],
    consumer_timeout_ms=10000
)

# Función para generar variables dummy y ajustar las columnas del DataFrame
def preprocess_data(df):
    # Generar variables dummy para "continent" y renombrarlas
    df = pd.get_dummies(df, columns=["continent"])
    rename_columns = {
        "continent_North America": "continent_North_America",
        "continent_Central America": "continent_Central_America",
        "continent_South America": "continent_South_America"
    }
    df = df.rename(columns=rename_columns)

    # Asegurar que todas las columnas esperadas por el modelo están presentes
    expected_columns = ['year', 'health', 'social_support', 'economy', 'corruption_perception', 
                        'freedom', 'generosity', 'continent_Africa', 'continent_Asia', 
                        'continent_Central_America', 'continent_Europe', 'continent_North_America', 
                        'continent_Oceania', 'continent_South_America']
    
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0  # Añadir columnas faltantes con valor 0

    # Ordenar columnas según el orden esperado por el modelo
    df = df[expected_columns]
    return df

batch_data = pd.DataFrame()

for message in consumer:
    data = message.value
    df = pd.DataFrame([data])

    # Preprocesar datos antes de predecir
    features = preprocess_data(df)
    
    # Realizar predicción
    df['predicted_happiness_score'] = model.predict(features)
    batch_data = pd.concat([batch_data, df], ignore_index=True)

    print(f"Predicted Happiness Score: {df['predicted_happiness_score'].values[0]}")

    # Insertar batch en PostgreSQL si se acumula suficiente data
    if len(batch_data) >= 20:
        try:
            batch_data.to_sql('happiness_predictions', engine, if_exists='append', index=False)
            print("Batch of data inserted successfully.")
        except Exception as e:
            print(f"Error inserting batch into PostgreSQL: {e}")
        batch_data = pd.DataFrame()  # Resetear batch_data después de la inserción

# Inserta los datos restantes que puedan quedar en el batch_data
if not batch_data.empty:
    try:
        batch_data.to_sql('happiness_predictions', engine, if_exists='append', index=False)
        print("Remaining data inserted successfully.")
    except Exception as e:
        print(f"Error inserting remaining data into PostgreSQL: {e}")

consumer.close()
print("Consumer closed.")