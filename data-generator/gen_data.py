import requests
import json
import datetime
import random

with open ("./.tinyb") as tinyb:
    tb = json.load(tinyb)
    token = tb['token']
    host = tb['host']

def send_events(ds: str, token: str, messages: list):
  params = {
    'name': ds,
    'token': token,
    'wait': 'false',
  }
  data = '\n'.join(json.dumps(m) for m in messages)
  r = requests.post(f'{host}/v0/events', params=params, data=data)
  # uncomment the following two lines in case you don't see your data in the datasource
  # print(data)
  # print(r.status_code)

params = {
    'token': token
}
while True:
# fetch latest values
  latest_values_url = f'https://api.tinybird.co/v0/pipes/last_price.json'
  response = requests.get(latest_values_url, params=params)

  resp_data = response.json()['data']

  for s in range(len(resp_data)):
    symbol = resp_data[s]['stock_symbol']
    price = resp_data[s]['price']
    date = datetime.datetime.strptime(resp_data[s]['ts'], '%Y-%m-%d %H:%M:%S') 
    # if date hour > 23:55:00, date = date + 8h: values stop from 23:59:59 to 8:00:00
    if (date.hour==23 and date.minute >= 55):
      date = date + datetime.timedelta(hours=8)
    stddev = resp_data[s]['stddev']
    sample = random.randint(20,120)
    t_deltas = [random.randint(1,300) for _ in range(sample)]
    t_deltas.sort()
    dates=[date + datetime.timedelta(seconds=d) for d in t_deltas]
    amounts = [round(random.gauss(price, stddev*2),2) for _ in range(sample)]
    nd = []
    for i in range(sample):
      message = {
        'stock_symbol': symbol,
        'date': dates[i].strftime('%Y-%m-%d %H:%M:%S'),
        'amount': amounts[i]
      }
      print(message)
      nd.append(message) 
    send_events(ds='prices', token=token, messages=nd)


