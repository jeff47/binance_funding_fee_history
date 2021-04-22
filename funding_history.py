#!/usr/bin/python3
import json
import requests
import csv
import pandas as pd
import argparse
import datetime as dt

# This will obtain the funding fee history from Binance for all the perpetual crypto contracts, for the given time period.
# Results will be saved in CSV format.
# All the data here is also available at https://www.binance.com/en/futures/funding-history/1, but the history is available
# only for single tokens at a time.

# How many days of history to get?  333 seems to be the max.
all_args = argparse.ArgumentParser()
all_args.add_argument("-d", "--days", required=True, type=int, help="Days of history to retrieve. 333 seems to be the maximum.")
all_args.add_argument("-s", "--span", default=9, required=False, type=int, help="Decay setting.  Higher numbers result in less weighting of recent rates. Defaults to 9 (96 hours).")
all_args.add_argument("-v", "--verbose", action="store_true", help="Print symbols as they are fetched.")

args = vars(all_args.parse_args())

days = args['days']
span = args['span']
verbose = args['verbose']

# Query the Binance API to get all the symbols available for arbitrage
page = requests.get('https://fapi.binance.com/fapi/v1/premiumIndex')
futures = json.loads(page.content)

# I'm not sure what these symbols are, but the API doesn't not return data for them and you can't trade them.
excludelist = ('ETHUSDT_210625', 'BTCUSDT_210625')

# Now query the Binance API again, fetching the history for each symbol
all_agg_df = pd.DataFrame()
all_data_df = pd.DataFrame()
for i in futures:
    if i["symbol"] in excludelist: continue
    if verbose: print(i["symbol"])
    page = requests.get('https://fapi.binance.com/fapi/v1/fundingRate', params={'symbol':i["symbol"],'limit':days*3})
    try:
        df = pd.DataFrame(json.loads(page.content))
        df = df.astype({'fundingRate': 'float64'})
    except:
        print("Could not parse data for symnbol " + i["symbol"])
        continue

    # Calculate Exponential weighted moving average
    df['EWMA'] = df['fundingRate'].ewm(span=span,adjust=False).mean()
    all_data_df = all_data_df.append(df)
    agg_df = df.groupby('symbol').fundingRate.agg(['mean', 'std', 'min', 'max', 'count'])
    agg_df.insert(0, 'EWMA', df['EWMA'].tail(1).to_string(index=False))
    all_agg_df = all_agg_df.append(agg_df)

rawdata_csv = "funding_fees_raw_" + str(days) + "d.csv"
aggdata_csv = "funding_fees_stats_" + str(days) + "d.csv"
all_agg_df.to_csv(aggdata_csv)
all_data_df.to_csv(rawdata_csv, index = False)

