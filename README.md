# binance_funding_fee_history
Get funding fee history information from Binance

This is a pretty simple python script designed to pull funding fee histories from Binance to aid in the creation of Spot-Arbitrage Bots on [Pionex](https://www.pionex.com).

The information is available via the web at [Binance](https://www.binance.com/en/futures/funding-history/0).  However, it is difficult to compare tokens side by side.  Instead, this script pulls the history going back a determined amount and displays the average funding fee, the stdev (to give a sense of its variation), the low and high so you can see if it's gone negative, as well as the number of historical data points used.

## Direct Link
If you don't want to run the script yourself, I try to keep a reasonably up-to-date spreadsheet on [Google Sheets]{https://docs.google.com/spreadsheets/d/1Dm56E7YEFBw7KFJ4EcmeMs-Ow65E_CmIBwBJoUO1-ig/edit?usp=sharing}.

## To-Do:
- Add some measure of the variability of the token itself.  This can be helpful to avoid tokens that come with higher risk of deleverage events, but I'm working on which stat to use still.

## Thanks to:
[xuefeng-huang](https://gist.github.com/xuefeng-huang) for adding the calculations to the script, rather than depending on Google Sheets.
