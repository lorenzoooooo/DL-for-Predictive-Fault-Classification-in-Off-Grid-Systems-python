# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 17:11:14 2022

@author: UTENTE
"""

from mezzanotte import mezzanotte
from toexcel import toexcel
import pandas as pd
import datetime as dt
import numpy as np
import globals

def estrazione_sequenze(p,nuova_struct,variabili):    
    globals.initialize()
    # Trovo le sequenze che sono più lunghe di 31 ore
    variabili_nb=list()                                                   # % contiene il nome delle variabili senza spazi
    for i in range(len(variabili)):
        variabili_nb.append(variabili[i].replace(" ",""))
    y=list()
    idx={}
    for j in variabili_nb:
        [dhour,d0]=mezzanotte(p[j]['time'])
        p[j].reset_index(drop=True,inplace=True)
        d0.reset_index(inplace=True, drop=True)
        tolleranza=7
        treshold=24 + tolleranza
        treshold=pd.to_timedelta(treshold, unit='h')
        err=list()
        for i in range(1,len(dhour)):
            d1=d0.iloc[i]-d0.iloc[i-1]
            if d1 > treshold:
                err.append(i)       #riporta l'indice di d0.iloc[i]
        
        # Ottengo sequenze di 24 ore
        temp=list()
        for i in range(len(dhour)):
            if i not in err: 
                temp.append(dhour[i])    
        idx[j]=p[j]['time'].iloc[temp]
        y.append(temp)
    x=list()
    for i in range(len(y)):
        x.append(len(y[i]))
    aa = max(range(len(x)), key=x.__getitem__)
    idx=idx[variabili_nb[aa]] 
    idx=pd.to_datetime(idx.astype(str)).dt.date                     # Scelgo il dato col maggiore numero di campioni così da escludere meno dati possibili dalle sequenze da prelevare e elimino i campi ora, minuto, secondo
    idx = idx.unique()                                              # cancello le ripetizioni
    idx=np.delete(idx,0,axis=0)
    seq={}
    counter=0
    for i in range(0,len(idx)-globals.span,globals.span):
        b=[]
        mystruct=pd.DataFrame()
        for j in range(globals.lasso):
            c=np.where(idx==idx[i]+dt.timedelta(days=j+1))
            if c[0].size==0:
                break
            b.append(c[0][0])
        if len(b)==globals.lasso:
            a=np.where(nuova_struct['time'].dt.date==idx[i])[0][0]
            c=np.where(nuova_struct['time'].dt.date==idx[i]+dt.timedelta(days=globals.lasso))[0][0]
            if (a.size!=0) & (c.size!=0):
                t=nuova_struct.loc[a:c,'time'].dt.strftime("%Y-%m-%d %H:%M")
                mystruct['time']=toexcel(t,"%Y-%m-%d %H:%M")
                for j in range(len(variabili_nb)):
                    mystruct[variabili_nb[j]]=nuova_struct.loc[a:c,variabili_nb[j]]
                seq[counter]=mystruct
                counter=counter+1
    return seq, variabili_nb