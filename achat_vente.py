# -*- coding: utf-8 -*-

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

from config import *
from fonctions import *




def main():
    
    star_time = to_timestamp(str(st.date_input('date de début',date_init ))) #1502928000000
    end_time = to_timestamp(str(st.date_input('date de fin')))
    delta_hour = '15m'
    #st.selectbox('selectionner une plage auraire',
                 #'4h','6h','8h','12h'])
   
    
      
    crypto = {}
    boxmax ={}
    market= np.array(['ADA/USDT','DOGE/USDT','BNB/USDT', 'ETH/USDT', 'DOT/USDT'])
    
    for elm in market :
        x =elm.lower()   
        crypto[x] = down_all_coin(elm ,star_time, end_time,delta_hour,exchange) #
        crypto[x]=pd.DataFrame(data=crypto[x], columns=['timestamp', x[:3]+'_open', 'high','low', x[:3]+'_close', 'volume']) 
        crypto[x] = crypto[x][['timestamp',x[:3]+'_open',x[:3]+'_close']]     
        #crypto[x] = convert_time(crypto[x])
        crypto[x] = crypto[x].set_index('timestamp')
    array_mauvais_shape = detection_mauvais_shape(crypto)
    crypto = correction_shape(crypto, array_mauvais_shape)
    for elm in array_mauvais_shape :
        crypto[elm]['timestamp'] = generation_date (crypto[elm], int(delta_hour[:1]))
        crypto[elm] =  crypto[elm].set_index('timestamp') 
    for elm in market : 
        x =elm.lower() 
        crypto[x] = crypto[x].merge(variation(crypto[x]),on ='timestamp',how='left')
        crypto[x]['coef_multi_'+x[:3]]=coef_multi(crypto[x])
        crypto[x]  = fonction_cumul(crypto[x],x) 
        
        
        
        
    df_liste_var =  fonction_tableau_var(crypto)   
    tableau_var = meilleur_varaition(df_liste_var) 
    
    tableau_var['algo'] = algo(tableau_var)
    tableau_var['coef_multi'] = tableau_var['algo'].cumprod()
    print(tableau_var)
  
   
    
    #tableau_var['algo'].apply(lambda x : (x*100)-100).cumprod()

    
   
    
    
  
    
    
    
    
    
if __name__ == '__main__':
    main()