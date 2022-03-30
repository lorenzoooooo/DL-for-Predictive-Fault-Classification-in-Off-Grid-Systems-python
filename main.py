# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 11:57:32 2022

@author: UTENTE
"""

import matplotlib.pyplot as plt
import pandas as pd
import pickle
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'


from estrazione_sequenze import estrazione_sequenze
from sospetti import sospetti
from normalizzazione import normalizzazione
from etichette import etichette
from dataset1 import dataset1

''' Per ogni traliccio '''

with open('mat.txt','r') as fileID:
    a=fileID.readline()
    a=a.rstrip('\n')
    while (isinstance(a, str)) & (len(a)!=0) :
        with open(a + 'dataset.csv','r') as data:
            torre=data.readline()
            addr=data.readline()
            data.close()
        addr=addr.rstrip('\n')
        RESULT=pickle.load(open(addr + torre.rstrip('\n') + '.pkl','rb'))
        # idx_g=RESULT['idx_g']
        # idx_b=RESULT['idx_b']
        # sequenze=RESULT['sequenze']
        p=RESULT['p']
        nuova_struct=RESULT['nuova_struct']
        nuova_struct['time']=pd.to_datetime(nuova_struct['time'].astype(str))
        variabili= ["min cell voltage", "panel power"]    #"tot battery current"
        
        [sequenze, variabili_nb]=estrazione_sequenze(p,nuova_struct,variabili)  # suddivido in sequenze di lasso giorni
        [idx_b,idx_g,c]=sospetti(sequenze)                                      # identifico le sequenze patologiche 
        sequenze=normalizzazione(nuova_struct,sequenze,variabili)              # sottraggo il valor medio e divido per la deviazione standard 
        [X,Y]=etichette(idx_b,idx_g,sequenze)
        
        RESULT['idx_b']=idx_b
        RESULT['idx_g']=idx_g
        RESULT['sequenze']= sequenze
        RESULT['variabili']=variabili
        RESULT['variabili_nb']=variabili_nb
        RESULT['X']=X
        RESULT['Y']=Y
        pickle.dump(RESULT, open(addr + torre.rstrip('\n') + '.pkl','wb'))
        a=fileID.readline()
        a=a.rstrip('\n')
    fileID.close()

''' dataset '''
dataset1()


# plt.figure()
# for i in idx_g:
#     plt.plot(sequenze[i]['time'],sequenze[i]['mincellvoltage'],linewidth=1)
# plt.title(torre + 'prev good')                    
# plt.figure()
# for i in idx_b:
#     plt.plot(sequenze[i]['time'],sequenze[i]['mincellvoltage'],linewidth=1)
# plt.title(torre + 'prev bad') 
# plt.figure()
# for i in c[0]:
#     plt.plot(sequenze[i]['time'],sequenze[i]['mincellvoltage'],linewidth=1)
# plt.title(torre + 'bad')
# plt.figure()
# for i in c[1]:
#     plt.plot(sequenze[i]['time'],sequenze[i]['mincellvoltage'],linewidth=1)
# plt.title(torre + 'good')