# Stock symbol and price extraction

## Description: 
Multi-threading by Inheriting thread class. 
### Steps:
1. Get all the NSE symbols from Wiki page - `workers/wikiWorker.py`
2. use multi-threading to get price of each symbol from Yahoo Finance - `workers/yahooFinanceWorker.py`
3. use Queue(supports multithreading) from multi-processing to get prices sequencially - 'main.py'
4. store the result in Queue and finally insert/update results to the `postgres` Database with multi-threading. - `workers/postgresWorker.py`