# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 10:32:10 2022

@author: UTENTE
"""
import numpy as np
import pandas as pd

def mezzanotte(tempo):
    d=pd.to_datetime(tempo.astype(str)).dt.hour
    
    ''' Trovo i campioni che scandiscono la fine della giornata'''
    lista=[18, 19, 20, 21, 22, 23, 0, 1, 2, 3]
    dhour=np.array([])
    for i in lista:
        a=np.where(d==i)
        dhour=np.concatenate((dhour,a[0]))
    dhour=np.sort(dhour)
    
    ''' voglio solo il primo campione alla fine di ogni giorno'''
    i=dhour[0]
    j=np.where(dhour==i)
    counter=1
    while i<dhour[-1]:
        e=dhour[(j[0]+1)]
        if e!=dhour[j[0]]+counter:
            i=dhour[j[0]+1]
            counter=1
            j=np.where(dhour==i)
        else:
            dhour=np.delete(dhour, j[0]+1, axis=0)
            counter=counter+1;
    d0=pd.to_datetime(tempo.iloc[dhour].astype(str))
    return dhour, d0
