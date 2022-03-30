# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 15:15:17 2022

@author: UTENTE
"""

def allineo(c,ref):
    start=[]
    finish=[]
    for i in range(len(c)):
        start.append(c[ref.iloc[i,0]]['time'].iloc[0])
        finish.append(c[ref.iloc[i,0]]['time'].iloc[-1])
    
    start=max(start)
    finish=min(finish)
    for i in range(len(c)):
        x=c[ref.iloc[i,0]]['time'].index[c[ref.iloc[i,0]]['time'].eq(start)]
        if x[0]>0:
            c[ref.iloc[i,0]].drop(list(range(0,x[0])), inplace=True)
            c[ref.iloc[i,0]] = c[ref.iloc[i,0]].sort_index().reset_index(drop=True)
        y=c[ref.iloc[i,0]]['time'].index[c[ref.iloc[i,0]]['time'].eq(finish)]
        if finish<c[ref.iloc[i,0]]['time'].iloc[-1]:
            c[ref.iloc[i,0]].drop(list(range(y[-1]+1,len(c[ref.iloc[i,0]]['time']))), inplace=True)  
            c[ref.iloc[i,0]] = c[ref.iloc[i,0]].sort_index().reset_index(drop=True)
    return c