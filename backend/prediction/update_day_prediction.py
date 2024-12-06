import pandas as pd
import requests
from io import StringIO
from prophet import Prophet

res = requests.get('http://database_api:8000/group/day/0?skip_current=true')
df = pd.read_json(StringIO(res.text))

df = df[['date', 'updated']]
df['date'] = pd.to_datetime(df['date'])
df = df.rename(columns={'date': 'ds', 'updated': 'y'})

model = Prophet()
model.fit(df)

future = model.make_future_dataframe(periods=1, include_history=False)
forecast = model.predict(future)

forecast['yhat'] = forecast['yhat'].round().astype(int)
forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

forecast = forecast.rename(columns={
    'ds': 'predict_day',
    'yhat': 'predict_value',
    'yhat_lower': 'lower_range',
    'yhat_upper': 'upper_range'
})

forecast['predict_day'] = forecast['predict_day'].dt.strftime('%Y-%m-%d')

requests.post("http://database_api:8000/prediction/day", 
    json=forecast.to_dict('records'),
    headers={"Content-Type": "application/json"},
)

print(forecast)
