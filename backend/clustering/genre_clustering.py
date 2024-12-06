import requests
import pandas as pd
from io import StringIO
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from datetime import datetime

res = requests.get('http://database_api:8000/group/genre/7')
df = pd.read_json(StringIO(res.text))

scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[["avg_score", "count"]])

kmeans = KMeans(n_clusters=4)
df["cluster"] = kmeans.fit_predict(scaled_data)
df = df[["genre", "count", "avg_score", "cluster"]]

current_day = datetime.now().strftime("%Y-%m-%d")
data = df.to_json(orient="records", force_ascii=False)
data = [{
    "updated_date": current_day,
    "clustering_data": data
}]

requests.post("http://database_api:8000/clustering/weeks", 
    json=data,
    headers={"Content-Type": "application/json"},
)
