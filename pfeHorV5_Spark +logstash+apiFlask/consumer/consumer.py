import json
from kafka import KafkaConsumer
from pymongo import MongoClient

# Connexion MongoDB (nom du service mongo dans Docker Compose)
mongo_client = MongoClient('mongodb://root:root@mongo:27017/admin')
db = mongo_client['logs_db']
collection = db['raw_logs']

# Configuration du consumer Kafka (nom du service kafka dans Docker Compose)
consumer = KafkaConsumer(
    'logs',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='mongo_consumer_group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    consumer_timeout_ms=10000  # Timeout 10s si aucun message
)

print("Démarrage du consumer Kafka -> MongoDB...")

try:
    for message in consumer:
        log = message.value
        print("Message reçu :", log)
        collection.insert_one(log)
        print("Log inséré dans MongoDB")
except Exception as e:
    print(f"Erreur : {e}")

print("Fin de la consommation (timeout atteint)")
