from kafka import KafkaProducer
import pandas as pd
import pickle
import json
import os

# Ruta al modelo entrenado
model_path = os.path.join(os.path.dirname(__file__), '../model/gb_model.pkl')
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Cargar los datos de prueba
test_data_path = os.path.join(os.path.dirname(__file__), '../clear_data/happiness_data.csv')
test_data = pd.read_csv(test_data_path)

# Configurar el productor de Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Realizar predicciones y enviarlas a Kafka
for _, row in test_data.iterrows():
    # Seleccionar las columnas de características
    features = row[['country', 'region', 'gdp_per_capita', 'healthy_life_expectancy', 
                    'freedom', 'perceptions_of_corruption', 'generosity']].to_dict()
    
    # Convertir a DataFrame y realizar la predicción
    features_df = pd.DataFrame([features])
    prediction = model.predict(features_df)[0]
    
    # Crear el mensaje
    message = {
        'features': features,
        'predicted_happiness_score': prediction
    }
    # Enviar el mensaje a Kafka
    producer.send('happiness_predictions', value=message)
    print("Predicción enviada a Kafka:", message)

producer.flush()
producer.close()
