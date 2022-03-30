# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 17:44:24 2022

@author: UTENTE
"""

def interpola(x):
    from scipy.interpolate import interp1d
    x=x.drop_duplicates(subset=['time'])
    idx=x['diag'].index[x['diag'].eq(0)]
    x=x.astype({"time":float,"value":float})
    x['value']=interp1d(x['time'][idx],x['value'][idx], fill_value="extrapolate")(x['time'])
    return x
    # gli ultimi valori se sono 0 lui li mette a NaN e quindi vanno forzati a 0
    # n=isnan(coord.value);
    # n=find(n==1);
    # coord.value(n)=y(n);