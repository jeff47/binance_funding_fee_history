#!/usr/bin/python3
import json
import requests
import csv
import pandas as pd
# %%
days = 90

# Get all the symbols available
page = requests.get('https://fapi.binance.com/fapi/v1/premiumIndex')
futures = json.loads(page.content)

# Fetch the history for each symbol.
history = []
for i in futures:
    page = requests.get('https://fapi.binance.com/fapi/v1/fundingRate', params={'symbol':i["symbol"],'limit':days*3})
    history += json.loads(page.content)
# %%
filename = "funding_fees.json"
with open(filename, 'w') as json_file:
    json_file.write('{"funding_data":')
    json.dump(history, json_file)
    json_file.write('}')
# %%
with open("funding_fees.json", 'r') as json_file:
    json_data = json.load(json_file)
# %%
fee_data = json_data['funding_data']
data_file = open('funding_fees.csv', 'w')
csv_writer = csv.writer(data_file)
# %%
header = fee_data[0].keys()
csv_writer.writerow(header)
for fee in fee_data:
    csv_writer.writerow(fee.values())

data_file.close()

df = pd.read_csv('funding_fees.csv')
agg_df = df.groupby('symbol').fundingRate.agg(['mean', 'std', 'min', 'max', 'count'])
agg_df.to_csv('agg_stats.csv')
