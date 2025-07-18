# Big-Data-Architecture-for-Automated-Detection-of-Unknown-Attacks-using-
Big Data Architecture for Automated Detection of Unknown Attacks using Spark, Kafka, and Distributed ML APIs


#Table of Contents

Project Overview

Architecture

Features

Technologies

Setup and Installation

Usage

Future Improvements

Contributing

*****************************************

#Project Overview
This project implements a scalable real-time network threat detection and enrichment system leveraging modern Big Data technologies and machine learning models. It streams network logs, applies supervised and unsupervised learning to detect known and unknown attacks, enriches event data, and indexes results for visualization and analysis.

The system uses a distributed architecture combining Kafka for messaging, Spark Structured Streaming for processing, Flask APIs for ML inference, Logstash for log transformation, and Elasticsearch Kibana for visualization.
******************************************
#Architecture
Kafka: Message broker for ingesting streaming network logs.

Spark Structured Streaming: Processes Kafka streams, enriches logs by calling ML prediction APIs.

Flask APIs: Hosts ML models (XGBoost for supervised detection; Isolation Forest for anomaly detection).

Logstash: Additional ingestion and enrichment, integrating with ELK stack.

Elasticsearch & Kibana: Stores enriched logs and provides dashboards for real-time monitoring.

MongoDB: Persists raw and processed logs for offline analysis.
******************************************
#Features
Real-time streaming ingestion of network logs.

Hybrid detection combining supervised classification and unsupervised anomaly detection.

Auto-enrichment of events with ML predictions via REST APIs.

Fault-tolerant, horizontally scalable architecture with containerization (Docker).

Visualization and alerting via Kibana dashboards.

Continuous integration capability to add unknown attacks for model retraining.
******************************************
#Technologies
Apache Kafka

Apache Spark (Structured Streaming)

Python Flask (ML REST API)

Docker & Docker Compose

Elasticsearch, Logstash, Kibana (ELK stack)

MongoDB

XGBoost & Scikit-learn

Isolation Forest
******************************************
#Setup and Installation
Clone the repo:

bash
git clone <repo_url>
cd <repo_folder>
Build and start services with Docker Compose:

bash
docker compose up -d --build
Verify all containers are running:

bash
docker ps
Access Kibana UI:
Navigate to http://localhost:5601
******************************************
#Usage
The simulator service produces network logs into Kafka topic logs.

Spark streaming app consumes logs, calls Flask ML APIs to get predictions, and writes enriched data to Elasticsearch.

Logstash further processes logs and pushes to ELK for visualization.

MongoDB stores raw logs for audit and offline analysis.

Kibana dashboards visualize normal and anomalous traffic, showing prediction results.
******************************************
#Future Improvements
Implement active learning loop : automatically add confirmed unknown attacks to training set and retrain models.

Optimize Spark UDFs for batch API calls to reduce latency.

Scale Flask APIs with Gunicorn and load balancing.

Integrate alerting system based on anomaly scoring thresholds.

Add user authentication and role-based access control to Kibana dashboards.


