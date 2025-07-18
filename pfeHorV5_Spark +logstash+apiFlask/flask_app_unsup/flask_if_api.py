# flask_unsupervised.py
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

model = joblib.load("isolation_forest_advanced.joblib")
scaler = joblib.load("scaler_if_advanced.joblib")
protocol_type_mapping = {"tcp": 0, "udp": 1, "icmp": 2}
service_mapping = {"http": 0, "ftp": 1, "smtp": 2}
flag_mapping = {"SF": 0, "REJ": 1, "RSTO": 2}
required_fields = [
    "duration", "protocol_type", "service", "flag",
    "src_bytes", "dst_bytes", "wrong_fragment", "hot",
    "logged_in", "num_compromised", "count", "srv_count",
    "serror_rate", "srv_serror_rate", "rerror_rate"
]

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400
        features = [
            float(data["duration"]),
            protocol_type_mapping.get(data["protocol_type"], -1),
            service_mapping.get(data["service"], -1),
            flag_mapping.get(data["flag"], -1),
            float(data["src_bytes"]),
            float(data["dst_bytes"]),
            float(data["wrong_fragment"]),
            float(data["hot"]),
            float(data["logged_in"]),
            float(data["num_compromised"]),
            float(data["count"]),
            float(data["srv_count"]),
            float(data["serror_rate"]),
            float(data["srv_serror_rate"]),
            float(data["rerror_rate"])
        ]
        if -1 in features[:4]:
            return jsonify({"error": "Invalid categorical value"}), 400
        features_scaled = scaler.transform([features])
        prediction = model.predict(features_scaled)[0]
        return jsonify({
            "prediction": int(prediction),
            "status": "anomaly" if prediction == -1 else "normal"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "Bienvenue sur l'API Flask - Détection Anomalies (Isolation Forest)"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)

