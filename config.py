# -*- coding: utf-8 -*-
from datetime import datetime
from time import time 
from datetime import timedelta
import numpy as np
import ccxt

date_init = datetime.now() - timedelta(days = 180)
 
exchange = ccxt.binance({'enableRateLimit': True})
exchange.load_markets()

liste_crypto1 = np.array(['BTC/USDT', 'ETH/USDT', 'ADA/USDT','DOGE/USDT', 'BNB/USDT', 'UNI/USDT',
                    'LTC/USDT', 'BCH/USDT', 'LINK/USDT', 'VET/USDT', 'XLM/USDT', 'FIL/USDT','TRX/USDT', 
                    'NEO/USDT','EOS/USDT','DOT/USDT'])
        
liste_crypto = np.array(['ADA/USDT','DOGE/USDT','BNB/USDT', 'ETH/USDT', 'DOT/USDT'])


"""
test en cas de beug 

# You ask for the balance
balance= client.get_asset_balance(asset='USDT')

# set the percentage or fraction you want to invest in each order
portion_balance = float(balance['free']) * 0.35

# you assign the created variable in the quantity of your order
sell_market = client.order_market_sell(
    symbol= 'ETHUSDT',
    quantity= portion_balance)


"""