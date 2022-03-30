# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 12:54:39 2022

@author: UTENTE
"""

from datetime import datetime
import pandas as pd

def fromexcel(t):
    b=[]    
    _epoch0=datetime(1899, 12, 31, 0 , 0, 0)
    for i in range(len(t)):
        if t[i] >= 60:
            t[i] -= 1                   # Excel leap year bug, 1900 is not a leap year!
        a=_epoch0 + pd.to_timedelta(t[i],'D')
        a=a.replace(second=0,microsecond=0)
        b.append(a)
    return b