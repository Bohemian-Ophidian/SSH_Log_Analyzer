from sklearn.ensemble import IsolationForest
import joblib

def train_model(X):
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(X)
    joblib.dump(model, "model/isolation_forest.pkl")


def detect_anomalies(X):
    model = joblib.load("model/isolation_forest.pkl")
    predictions = model.predict(X)
    return predictions

