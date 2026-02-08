from fastapi import FastAPI

app = FastAPI()

trading_accounts = [
   { "id": 0, "name": "test1", "balance": 10000}, 
   { "id": 1, "name": "test2", "balance": 20000}
   ]
trade_list = [
    {"id": 0, "account_id": 0, "symbol": "EURUSD", "type":"buy", "size": 0.01, "entryprice": 1.0000, "exitprice": 2.0000},
    {"id": 1, "account_id": 1, "symbol": "GBPUSD", "type":"sell", "size": 0.25, "entryprice": 1.0400, "exitprice": 1.0070},
    {"id": 2, "account_id": 0, "symbol": "XAUUSD", "type":"buy", "size": 0.25, "entryprice": 1.0400, "exitprice": 1.0070},
    {"id": 3, "account_id": 1, "symbol": "USDJPY", "type":"sell", "size": 0.25, "entryprice": 1.0400, "exitprice": 1.0070}
    ]

@app.get("/accounts")
def get_all_accounts():
   return trading_accounts

@app.get("/accounts/{account_id}")
def get_single_account(account_id: int):
   for account in trading_accounts:
      if account["id"] == account_id:
         return account
    
   return {"error": "Account not found"}

@app.get("/trades")
def get_all_trades():
   return trade_list

@app.get("/trades/account{account_id}")
def get_trades_account(account_id: int):
    trades_account = []
    for trade in trade_list:
      if trade["account_id"] == account_id:
         trades_account.append(trade)
    
    if trades_account:
       return trades_account
    
    return {"error": "No trades found for this account."}

@app.get("/trade/{trade_id}")
def get_trade(trade_id: int):
    for trade in trade_list:
       if trade["id"] == trade_id:
          return trade
    
    return {"error": "No trade found with given id."}