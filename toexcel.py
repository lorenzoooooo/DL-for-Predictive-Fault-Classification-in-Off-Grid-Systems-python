# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 17:19:12 2022

@author: UTENTE
"""
import datetime as dt

def toexcel(t,f):
    temp = dt.datetime(1899,12,30,0,0,0,0)    # Note, not 31st Dec but 30th!
    for i in range(len(t)):
        t.iloc[i]=dt.datetime.strptime(t.iloc[i],f)
        delta = t.iloc[i] - temp
        t.iloc[i]= float(delta.days) + (float(delta.seconds) / 86400)
    return t