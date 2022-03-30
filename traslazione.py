# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 17:41:24 2022

@author: UTENTE
"""
import numpy as np
from inserisci import inserisci

def traslazione (c, max_timeout, std_freq):
    p=np.diff(c['time'])
    p=np.where(p>max_timeout)
    c = c.sort_index().reset_index(drop=True)
    for i in range(len(p[0])):
        c = inserisci(c,int(p[0][i]),std_freq);
    c = c.sort_index().reset_index(drop=True)
    return c