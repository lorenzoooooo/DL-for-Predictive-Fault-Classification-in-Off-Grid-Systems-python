# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:04:59 2022

@author: UTENTE
"""
import pandas as pd
# import numpy as np
def etichette(idx_b,idx_g, sequenze):
    seq={}
    # X={}
    X=list()
    Y=list()
    k=0
    for j in range(len(sequenze)):
        seq[j]=sequenze[j].drop('time',axis=1, inplace=False)
        if j in idx_b:
            X.append(pd.DataFrame(seq[j]).to_numpy())
            Y.append('0')
            k=k+1
        elif j in idx_g:
            X.append(pd.DataFrame(seq[j]).to_numpy())
            Y.append('1')
            k=k+1
    return X,Y