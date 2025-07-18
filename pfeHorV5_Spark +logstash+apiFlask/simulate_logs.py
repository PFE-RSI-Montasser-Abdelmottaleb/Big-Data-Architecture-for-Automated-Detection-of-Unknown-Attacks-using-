import logging
import json
import random
import time
from datetime import datetime, timezone
from kafka_handler import KafkaLogHandler

protocols = ["tcp", "udp", "icmp"]
services = ["http", "ftp", "smtp"]
flags = ["SF", "REJ", "RSTO"]

def timestamp():
    return datetime.now(timezone.utc).isoformat()

def generate_log():
    r = random.random()
    if r < 0.6:
        return {
            "timestamp": timestamp(),
            "duration": random.randint(1, 50),
            "protocol_type": random.choice(protocols),
            "service": random.choice(services),
            "flag": random.choice(flags),
            "src_bytes": random.randint(100, 1500),
            "dst_bytes": random.randint(100, 5000),
            "wrong_fragment": 0,
            "hot": 0,
            "logged_in": 1,
            "num_compromised": 0,
            "count": random.randint(1, 30),
            "srv_count": random.randint(1, 30),
            "serror_rate": 0.0,
            "srv_serror_rate": 0.0,
            "rerror_rate": 0.0,
            "label": "NORMAL"
        }
    elif r < 0.75:
        return {
            "timestamp": timestamp(),
            "duration": random.randint(1, 10),
            "protocol_type": "tcp",
            "service": "http",
            "flag": "REJ",
            "src_bytes": random.randint(0, 100),
            "dst_bytes": random.randint(0, 100),
            "wrong_fragment": 0,
            "hot": 0,
            "logged_in": 0,
            "num_compromised": random.randint(1, 3),
            "count": random.randint(80, 100),
            "srv_count": random.randint(80, 100),
            "serror_rate": 1.0,
            "srv_serror_rate": 1.0,
            "rerror_rate": 0.0,
            "label": "KNOWN_ATTACK"
        }
    elif r < 0.9:
        return {
            "timestamp": timestamp(),
            "duration": random.randint(100, 300),
            "protocol_type": random.choice(protocols),
            "service": "smtp",
            "flag": "RSTO",
            "src_bytes": random.randint(2000, 3000),
            "dst_bytes": random.randint(1000, 4000),
            "wrong_fragment": 1,
            "hot": 1,
            "logged_in": 0,
            "num_compromised": random.randint(5, 10),
            "count": random.randint(90, 100),
            "srv_count": random.randint(90, 100),
            "serror_rate": 0.9,
            "srv_serror_rate": 0.9,
            "rerror_rate": 0.3,
            "label": "ZERO_DAY"
        }
    else:
        return {
            "timestamp": timestamp(),
            "duration": random.randint(0, 300),
            "protocol_type": random.choice(protocols),
            "service": random.choice(services),
            "flag": random.choice(flags),
            "src_bytes": random.randint(0, 5000),
            "dst_bytes": random.randint(0, 5000),
            "wrong_fragment": random.randint(0, 1),
            "hot": random.randint(0, 1),
            "logged_in": random.randint(0, 1),
            "num_compromised": random.randint(0, 10),
            "count": random.randint(1, 100),
            "srv_count": random.randint(1, 100),
            "serror_rate": round(random.uniform(0, 1), 2),
            "srv_serror_rate": round(random.uniform(0, 1), 2),
            "rerror_rate": round(random.uniform(0, 1), 2),
            "label": "POLYMORPHIC_ATTACK"
        }

class JsonFormatter(logging.Formatter):
    def format(self, record):
        # Convertit le message dict en JSON string
        if isinstance(record.msg, dict):
            record.msg = json.dumps(record.msg)
        return super().format(record)

def main():
    logger = logging.getLogger("SimulateurKafka")
    logger.setLevel(logging.INFO)

    kafka_handler = KafkaLogHandler(
        bootstrap_servers=['kafka:9092'],
        topic='logs'
    )
    kafka_handler.setFormatter(JsonFormatter())
    logger.addHandler(kafka_handler)

    print("[SIMULATEUR] Démarrage et connexion à Kafka via logging handler...")

    while True:
        log = generate_log()
        logger.info(json.dumps(log))  # Convertit dict en JSON string avant d’envoyer
        print(f"[+] Log généré et envoyé à Kafka: {log}")
        time.sleep(0.06)

if __name__ == "__main__":
    main()
