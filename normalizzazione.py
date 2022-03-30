# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 11:18:16 2022

@author: UTENTE
"""
import numpy as np
import datetime as dt
import statistics
from fromexcel import fromexcel

def normalizzazione(nuova_struct,sequenze,variabili):
    media=[]
    dev_std=[]
    a=fromexcel([sequenze[0]['time'].iloc[0]])
    start=np.where(nuova_struct['time']==a[0])[0][0]
    b=fromexcel([sequenze[len(sequenze)-1]['time'].iloc[-1]])
    finish=np.where(nuova_struct['time']==b[0])[0][0]
    variabili_nb=list() 
    for i in range(len(variabili)):
        variabili_nb.append(variabili[i].replace(" ",""))
    for j in range(len(variabili_nb)):
        media.append(statistics.mean(nuova_struct[variabili_nb[j]].iloc[start:finish]))
        dev_std.append(statistics.stdev(nuova_struct[variabili_nb[j]].iloc[start:finish]))
    for i in range(len(sequenze)):
        for k in range(len(variabili_nb)):
            sequenze[i][variabili_nb[k]]=(sequenze[i][variabili_nb[k]]-media[k])/dev_std[k]
    
    return sequenze