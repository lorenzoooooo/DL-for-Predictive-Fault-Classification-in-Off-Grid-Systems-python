# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 10:39:48 2022

@author: UTENTE
"""
import globals
import numpy as np

def sospetti (sequenze):
    globals.initialize()
    idx_b=[]
    idx_g=[]
    
    ''' Prendo solo le sequenze a 7 giorni precisi da tutti gli eventi di guasto. Ossia se ho sequenze consecutive in bad.idx le tengo tutte e prendo per ognuna la sequenza 7 giorni prima'''
    if 'mincellvoltage' in sequenze[0].columns:
        a={}
        mincellv={}
        mincellv['soglia']=globals.soglia_bad_mincellv   # soglia critica patologica
        mincellv['bad_idx']=[]
        mincellv['good_idx']=[]
        for i in range(len(sequenze)):
            z,=np.where(sequenze[i]['mincellvoltage']<=mincellv['soglia'])
            if len(z)!=0:
                mincellv['bad_idx']=[*mincellv['bad_idx'], i]
            else:
                mincellv['good_idx']=[*mincellv['good_idx'], i]
        a[0]=mincellv['bad_idx']
        a[1]=mincellv['good_idx']
    
    
    '''prendo le sequenze dalla prima fino all'ultima di bad.mincellv '''
    z=list()
    for i in range(len(sequenze)):
        z.append(sequenze[i]['time'].iloc[0])
    z=np.array(z)
    counter=0
    for i in range(len(sequenze)):
        if i in mincellv['bad_idx']:
            if i > globals.int_predizione: 
                x=sequenze[i]['time'].iloc[0]-globals.int_predizione
                y=np.where(z==x)[0]
                if y.size!=0:
                    idx_b=[*idx_b, y[0]]
            counter=counter+1
    idx_b=list(dict.fromkeys(idx_b))    
    
    counter=0
    for i in range(len(sequenze)):
        if i in mincellv['good_idx']:
            if i > globals.int_predizione:
                x=sequenze[i]['time'].iloc[0]-globals.int_predizione
                y=np.where(z==x)[0]
                if y.size!=0:
                  idx_g=[*idx_g, y[0]]
            counter=counter+1
    idx_g=list(dict.fromkeys(idx_g))
    
    if len(idx_g)>(globals.proporzione*len(idx_b)):
        idx_g=np.random.choice(idx_g,globals.proporzione*len(idx_b))
        
    return idx_b, list(idx_g), a