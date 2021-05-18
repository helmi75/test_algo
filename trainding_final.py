# -*- coding: utf-8 -*-

import pandas as pd
import os
import numpy as np
import pickle
import matplotlib.pyplot as plt 
from datetime import datetime
from time import time 
from datetime import timedelta
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import base64
import ccxt
from fonctions import *
import time as tm



 
crypto ={}
market=['ETH/USDT','BTC/USDT','UNI/USDT','BNB/USDT','ADA/USDT','KSM/USDT']

delta_hour = '1m'
exchange = ccxt.binance({
    'apiKey': '7C9o9B0agRvuQkB8To0zqygf8cPIslFxXazbIMDFW6oFrVDRvC6OemFR60qU8n2n',
    'secret': 'dpaQJ2TYHmdPkM5cCVtwOl7aAcJuZPIyOkAmkDCwdvDFo7VHqFTczY0LxYKLuow5',
    'enableRateLimit': True
    })
st.write("wech bien ou quoi ? ")

# initialisation temps 

start_time = datetime.now()
k=0
liste_principale=[]
liste_achat=[]
liste_vente=[]
temps=[]



while True:
    
    print("première iteration  : ",start_time)   
    print("horaire now",datetime.now())
    print ("iteration numéto : ", k)
    
    st.write("première iteration  : ",start_time) 
    st.write("horaire now", datetime.now())
    st.write("iteration numéto : ", k)
    
    
    for elm in market :
        x =elm.lower()
        ohlcv = exchange.fetch_ohlcv(elm , limit = 2, timeframe = delta_hour)
        crypto[x] = pd.DataFrame(ohlcv,columns=['timestamp', x[:3]+'_open', 'high','low', x[:3]+'_close', 'volume'])
        crypto[x] = convert_time(crypto[x])
        crypto[x] = crypto[x][['timestamp',x[:3]+'_open',x[:3]+'_close']] 
        crypto[x] = crypto[x].set_index('timestamp')
        crypto[x] = crypto[x].merge(variation(crypto[x]),on ='timestamp',how='left')
        crypto[x]['coef_multi_'+x[:3]]=coef_multi(crypto[x])
        crypto[x]  = fonction_cumul(crypto[x],x)
                
    
    df_liste_var =  fonction_tableau_var(crypto)   
    tableau_var = meilleur_varaition(df_liste_var) 
    tableau_var['algo'] = algo(tableau_var)
    tableau_var['coef_multi'] = tableau_var['algo'].cumprod()
    nom_crypto_achat =  nom_crypto_achat_vente(tableau_var)
    nom_crypto_vente= crypto_a_vendre(exchange,2, market ) 
    print('la crypot à acheter est ',nom_crypto_achat)
    
    algo_achat_vente(exchange, nom_crypto_vente, nom_crypto_achat)
    
    k=k+1
    liste_principale.append([datetime.now(), nom_crypto_achat, nom_crypto_vente])
    st.write(tableau_var)
    st.write(pd.DataFrame(liste_principale, columns=['temps','crypto achat','crypto vente']))
    
    
    tm.sleep(5*60)
      
    


# =============================================================================
# 
# s = 2
# var1 =crypto_a_vendre[:-5]
# var2 = 'UNI'
# 
# #Vendre 
# sell = vente (exchange, var1, balence['total'])
# print(sell)
# 
# tm.sleep(5)    
# 
# #achat
# achat = achat(exchange ,var2, balence['total'])
# 
# 
# print(achat)
# 
# 
# =============================================================================




    
    
