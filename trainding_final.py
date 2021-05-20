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
import plotly.graph_objects as go
import base64
import ccxt
from fonctions import *
import time as tm



 
crypto ={}
market=['ETH/USDT','BTC/USDT','UNI/USDT']
apiKey = '7C9o9B0agRvuQkB8To0zqygf8cPIslFxXazbIMDFW6oFrVDRvC6OemFR60qU8n2n'
secret = 'dpaQJ2TYHmdPkM5cCVtwOl7aAcJuZPIyOkAmkDCwdvDFo7VHqFTczY0LxYKLuow5'



dth= '15m'
i_iteration = 2

delta_hour = dth


exchange = ccxt.binance({
    'apiKey': apiKey,
    'secret': secret,
    'enableRateLimit': True
    })
print( 'mimi')

# initialisation temps 

start_time = datetime.now()
k=0
liste_principale=[]
liste_achat=[]
liste_vente=[]
temps=[]
dpaQJ2TYHmdPkM5cCVtwOl7aAcJuZPIyOkAmkDCwdvDFo7VHqFTczY0LxYKLuow5

while True:

        print("première iteration  : ",start_time)   
        print("horaire now",datetime.now())
        print ("iteration numéto : ", k)

       


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
           print(crypto[x])

        df_liste_var =  fonction_tableau_var(crypto)   
        tableau_var = meilleur_varaition(df_liste_var) 
        tableau_var['algo'] = algo(tableau_var)
        tableau_var['coef_multi'] = (tableau_var['algo'].cumprod()*100)-100
        nom_crypto_achat =  nom_crypto_achat_vente(tableau_var)
        nom_crypto_vente= crypto_a_vendre(exchange,2, market ) 
        
        algo_achat_vente(exchange, nom_crypto_vente, nom_crypto_achat)
        
        print('la crypot à vendre est ',nom_crypto_vente)
        print('la crypot à acheter est ',nom_crypto_achat)


        k=k+1
        liste_principale.append([datetime.now(), nom_crypto_achat, nom_crypto_vente])
        print(tableau_var)
        print(pd.DataFrame(liste_principale, columns=['temps','crypto vente','crypto achat']))
        
        if nom_crypto_achat ==  nom_crypto_vente:
            st.write('On reste sur la même crypto')
        else:
           print('crypto à vendre ',nom_crypto_vente)
           print('crypto à acheter',nom_crypto_achat)
       


        tm.sleep(60*i_iteration)

    




    
    
