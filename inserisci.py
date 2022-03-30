# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 10:33:20 2022

@author: UTENTE
"""

def inserisci(a,x,std_freq):
    a.loc[x+0.5]=a['value'].iloc[x], a['time'].iloc[x+1]-std_freq, a['diag'].iloc[x]
    return a