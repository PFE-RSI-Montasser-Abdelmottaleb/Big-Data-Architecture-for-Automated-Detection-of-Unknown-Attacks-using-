from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, struct, to_json, udf
from pyspark.sql.types import StructType, StringType, IntegerType, DoubleType
import requests
import json


schema = StructType() \
    .add("timestamp", StringType()) \
    .add("duration", IntegerType()) \
    .add("protocol_type", StringType()) \
    .add("service", StringType()) \
    .add("flag", StringType()) \
    .add("src_bytes", IntegerType()) \
    .add("dst_bytes", IntegerType()) \
    .add("wrong_fragment", IntegerType()) \
    .add("hot", IntegerType()) \
    .add("logged_in", IntegerType()) \
    .add("num_compromised", IntegerType()) \
    .add("count", IntegerType()) \
    .add("srv_count", IntegerType()) \
    .add("serror_rate", DoubleType()) \
    .add("srv_serror_rate", DoubleType()) \
    .add("rerror_rate", DoubleType()) \
    .add("label", StringType())

spark = SparkSession.builder.appName("KafkaSparkToElasticsearch").getOrCreate()

# UDF appel API Flask (met connexion 'flask_sup-1' et 'flask_unsup-1' selon docker-compose)
def enrich_supervised(row_json):
    try:
        resp = requests.post(
            "http://flask_sup-1:5001/predict",
            headers={"Content-Type": "application/json"},
            data=row_json, timeout=2
        )
        if resp.ok:
            return resp.json().get("prediction")
        else:
            return None
    except Exception as e:
        return None

def enrich_unsupervised(row_json):
    try:
        resp = requests.post(
            "http://flask_unsup-1:5002/predict",
            headers={"Content-Type": "application/json"},
            data=row_json, timeout=2
        )
        if resp.ok:
            return resp.json().get("status")
        else:
            return None
    except Exception:
        return None

enrich_supervised_udf = udf(enrich_supervised, StringType())
enrich_unsupervised_udf = udf(enrich_unsupervised, StringType())


df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "logs") \
    .option("startingOffsets", "latest") \
    .load()

logs = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Par simplification ici, on n’applique pas d’UDF
logs_json = logs.withColumn("as_json", to_json(struct([col(c) for c in logs.columns])))


# Enrichissement supervisionné
logs_predict = logs_json.withColumn("prediction", enrich_supervised_udf(col("as_json")))

# Enrichissement non supervisionné
logs_predict = logs_predict.withColumn("anomaly_status", enrich_unsupervised_udf(col("as_json")))


query = logs_predict.writeStream.format("org.elasticsearch.spark.sql") \
    .option("es.nodes", "elasticsearch") \
    .option("es.port", "9200") \
    .option("es.resource", "logs_enriched") \
    .option("checkpointLocation", "/tmp/spark-es-checkpoint") \
    .option("es.net.ssl", "false") \
    .outputMode("append") \
    .trigger(processingTime="5 seconds") \
    .start()


print("Streaming started. Waiting for termination.")
query.awaitTermination()
print("Streaming terminated.")  # ne doit pas apparaitre sauf arrêt manuel


