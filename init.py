# # -*- coding: utf-8 -*-
# """
# Spyder Editor

# This is a temporary script file.
# """

import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
import datetime as dt
import csv
import pickle

from toexcel import toexcel
from interpola import interpola
from traslazione import traslazione
from sovracampiona import sovracampiona
from fromexcel import fromexcel 
from allineo import allineo


name=input('se la box NON è munita di stazione meteo scrivi var_iotbox, sennò var:')
ref = pd.read_excel (r'C:\\Users\\UTENTE\\Desktop\\py\\' + name + '.xlsx', names= ['variabile','codice'], header=None)
torre=input('numero della torre preceduto da t:')

if name == "var":
    tipo=input('Se è un digil puro scrivi digil senno scrivi iotbox-digil:');
    if not os.path.isdir(tipo):
        os.mkdir(tipo)
    if not os.path.isdir(tipo + "\\" + torre):
        os.mkdir(tipo + "\\" + torre)
elif name == "var_iotbox":
    tipo="iotbox";
    if not os.path.isdir(tipo):
        os.mkdir(tipo)
    if not os.path.isdir(tipo + "\\" + torre):
        os.mkdir(tipo + "\\" + torre)

columns= ['timestamp', 'count', 'codice', 'diag']
sqldata=pd.read_excel(r'C:\\Users\\UTENTE\\Desktop\\py\\' + tipo + "\\" + torre + '\\sqldata_grezzo.xlsx',names= columns, header=None)
# sqldata=pd.read_csv(r'C:\\Users\\UTENTE\\Desktop\\py\\' + tipo + "\\" + torre + '\\prova.csv',sep=';',index_col=None, header=None)

if torre == "t13008":
    t=sqldata.index[sqldata.eq('2021-08-11 00:38:53.0').any(1)]
    sqldata.drop(list(range(0,t[0])), inplace=True);
    sqldata.reset_index(drop=True,inplace=True)
    t=sqldata.index[sqldata.eq('2022-01-07 00:09:14.0').any(1)]
    sqldata.drop(list(range(t[-1]+1,len(sqldata))), inplace=True);
    sqldata.reset_index(drop=True,inplace=True)
elif torre == "t1025":
    t=sqldata.index[sqldata.eq('2021-07-02 00:09:27.0').any(1)]
    sqldata.drop(list(range(0,t[0])), inplace=True);
    sqldata.reset_index(drop=True,inplace=True)
elif torre == "t16399":
    t=sqldata.index[sqldata.eq('2021-09-23 00:07:31.0').any(1)]
    sqldata.drop(list(range(0,t[0])),inplace=True);
    sqldata.reset_index(drop=True,inplace=True)
    t1=sqldata.index[sqldata.eq('2021-11-18 16:08:53.0').any(1)]
    sqldata.drop(list(t1), inplace=True);
    sqldata.reset_index(drop=True,inplace=True)
elif torre == "t7286":
    t=sqldata.index[sqldata.eq('2021-12-27 04:45:30.0').any(1)]
    sqldata.drop(list(range(0,t[0])), inplace=True);
    sqldata.reset_index(drop=True,inplace=True)

tempo = sqldata.loc[:,'timestamp'];
tempo=tempo.copy()
tempo.rename("tempo",inplace=True)
format = "%Y-%m-%d %H:%M:%S.%f"
tempo=toexcel(tempo,format)
bozza_dati = pd.concat([tempo, sqldata["count"], sqldata["codice"], sqldata["diag"]],axis=1)
bozza_dati=bozza_dati.T
# %%

std_freq=(60*15)/86400;             # 15 min
max_timeout=(60*20)/86400;          # 20 min
final_freq=60/86400;                # 1 min

coord={}
for i in range(len(ref)):
    idx=bozza_dati.iloc[2,:].index[bozza_dati.iloc[2,:].eq(ref.loc[i,'codice'])]
    mystruct={}
    mystruct["value"]= bozza_dati.loc['count',idx]
    mystruct["time"]= bozza_dati.loc['tempo',idx]
    mystruct["diag"]= bozza_dati.loc['diag',idx]
    mystruct=pd.DataFrame(mystruct)
    coord[ref.iloc[i,0]]= mystruct

p={}
for i in range(len(coord)):
    coord[ref.iloc[i,0]] = interpola(coord[ref.iloc[i,0]])
    p[ref.iloc[i,0]] = coord[ref.iloc[i,0]]
    p[ref.iloc[i,0]] = p[ref.iloc[i,0]].copy()
    p[ref.iloc[i,0]]['time'] = fromexcel(pd.Series.to_numpy(p[ref.iloc[i,0]]['time']))
    coord[ref.iloc[i,0]] = traslazione(coord[ref.iloc[i,0]],max_timeout, std_freq)
    coord[ref.iloc[i,0]] = sovracampiona(coord[ref.iloc[i,0]],final_freq)
    coord[ref.iloc[i,0]] = coord[ref.iloc[i,0]].sort_index().reset_index(drop=True)

coord = allineo(coord,ref)

nuova_struct=pd.DataFrame(coord['irradiation']['time'],columns=['time'])
refx=ref
refx=refx.copy()
for i in range(len(ref)):
    refx.iloc[i,0]=ref.iloc[i,0].replace(" ","")
    coord[refx.iloc[i,0]]=coord.pop(ref.iloc[i,0])
    p[refx.iloc[i,0]]=p.pop(ref.iloc[i,0])
    nuova_struct = pd.concat([nuova_struct, coord[refx.iloc[i,0]]['value']], axis=1)
    nuova_struct = nuova_struct.rename(columns= {'value':refx.iloc[i,0]})


addr= tipo + "\\" + torre + "\\"
pickle.dump({'tipo': tipo, 'name':name, 'nuova_struct':nuova_struct, 'p':p}, open(addr + torre.rstrip('\n') + '.pkl','wb'))
with open(addr + 'dataset.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([torre])
    writer.writerow([addr])
    
# # % 
# # % for i=1:size(coord,1)
# # %     figure;
# # % %     plot(p{i,1}.time,p{i,1}.value,'r');
# # % %     hold on;
# # %     plot(coord{i,1}.time, coord{i,1}.value,'b');
# # %     title(coord{i,1}.name);
# # % %     hold off;
# # % end
 
