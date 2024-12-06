import pandas as pd
import requests
from io import StringIO
from prophet import Prophet

res = requests.get('http://database_api:8000/group/hour/0?skip_current=true')
df = pd.read_json(StringIO(res.text))

df['date_hour'] = pd.to_datetime(df['date_hour'])
df = df.rename(columns={'date_hour': 'ds', 'updated': 'y'})

model = Prophet()
model.fit(df)

future = model.make_future_dataframe(periods=3, freq='h', include_history=False)
forecast = model.predict(future)

forecast['yhat'] = forecast['yhat'].round().astype(int)
forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

forecast = forecast.rename(columns={
    'ds': 'predict_hour',
    'yhat': 'predict_value',
    'yhat_lower': 'lower_range',
    'yhat_upper': 'upper_range'
    })

forecast['predict_value'] = forecast['predict_value'].apply(lambda x: max(x, 1))

forecast['predict_hour'] = forecast['predict_hour'].dt.strftime('%Y-%m-%d %H')

requests.post("http://database_api:8000/prediction/hour",
    json=forecast.to_dict('records'),
    headers={"Content-Type": "application/json"},
)

print(forecast)
