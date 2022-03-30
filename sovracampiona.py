# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 12:40:46 2022

@author: UTENTE
"""

from scipy.interpolate import interp1d
import numpy as np
import pandas as pd
from fromexcel import fromexcel

def sovracampiona(c,final_freq):
    ds=1/86400  # 1 secondo
    x=c['time']
    x=x.copy()
    y=c['value']
    y=y.copy()
    z=np.arange(x.iloc[0],x.iloc[-1],ds)
    z=np.delete(z,-1)
    a=interp1d(x,y,fill_value='extrapolate')(z)
    b=np.arange(x.iloc[0],x.iloc[-1],final_freq)
    d=interp1d(z,a)(b)
    b=fromexcel(b)
    c=pd.DataFrame({'value': d, 'time': b})
    return c