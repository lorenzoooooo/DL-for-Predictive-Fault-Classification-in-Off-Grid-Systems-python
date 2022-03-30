# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 14:51:43 2022

@author: UTENTE
"""

import globals
import numpy as np
import pickle
import os
import tensorflow as tf

def dataset1():
    globals.initialize()
    Y_sane=list()
    X_sane=list()
    Y_patologiche=list()
    X_patologiche=list()
    tralicci=list()
    XTest=list()
    XTrain=list()
    YTest=list()
    YTrain=list()
    
    with open('mat.txt','r') as fileID:
        a=fileID.readline()
        a=a.rstrip('\n')
        while (isinstance(a, str)) & (len(a)!=0) :                                         #ciclo che prende i dati di una torre per volta
            with open(a + 'dataset.csv','r') as data:
                torre=data.readline()
                addr=data.readline()
                data.close()
            addr=addr.rstrip('\n')
            RESULT=pickle.load(open(addr + torre.rstrip('\n') + '.pkl','rb'))
            X=RESULT['X']
            Y=RESULT['Y']
            sane = [i for i, x in enumerate(Y) if x == '1']
            patologiche = [i for i, x in enumerate(Y) if x == '0']
            # b=X_sane.shape
            # c=X_patologiche.shape
            for i in range(len(sane)):
                X_sane.append(X[sane[i]])
                Y_sane=[*Y_sane, '1']
            for i in range(len(patologiche)):
                X_patologiche.append(X[patologiche[i]])
                Y_patologiche=[*Y_patologiche, '0']
            tralicci=[*tralicci, torre]                          
            a = fileID.readline()
            a=a.rstrip('\n')
        variabili_nb=RESULT['variabili_nb']
        fileID.close()
        
        ''' partizione dinamica '''
        Y=[*Y_sane, *Y_patologiche]
        Y=tf.convert_to_tensor(Y)
        X=[*X_sane, *X_patologiche]
        X=tf.convert_to_tensor(X)
        
        ''' partizione statica '''
        x=range(len(X_sane))
        a=np.random.choice(x,int(round(globals.rapporto*len(x),0)),replace=False)
        y=range(len(X_patologiche))
        b=np.random.choice(y,int(round(globals.rapporto*len(y),0)),replace=False)
        for i in range(len(a)):
            XTest.append(X_sane[a[i]])
            YTest=[*YTest, 1]
        for i in range(len(b)):
            XTest.append(X_patologiche[b[i]])
            YTest=[*YTest, 0]
        for i in range(len(x)):
            if i not in a:
                XTrain.append(X_sane[i])
                YTrain=[*YTrain, 1]
        for i in range(len(y)):
            if i not in b:
                XTrain.append(X_patologiche[i])
                YTrain=[*YTrain, 0]
        YTrain=tf.convert_to_tensor(YTrain)
        YTest=tf.convert_to_tensor(YTest)
        XTrain=tf.convert_to_tensor(XTrain)
        XTest=tf.convert_to_tensor(XTest)
                               
        ''' salvataggio'''
        stringa=''
        for i in range(len(tralicci)):
            stringa=stringa+tralicci[i].rstrip('\n')+'_'
        tralicci=''
        tralicci=stringa[:-1]
        stringa=''
        for i in range(len(variabili_nb)):
            stringa=stringa+variabili_nb[i].rstrip('\n')+'_'
        features=stringa[:-1]
        parametri=str(globals.lasso)+'_'+ str(globals.span)+'_'+str(globals.int_predizione)+'_'+str(globals.proporzione)+'_'+str(globals.rapporto)
        path=r'risultati_int\\' + tralicci + "\\" + features + "\\" + parametri + "\\"
        if not os.path.isdir('risultati_int'):
            os.mkdir('risultati_int')
        if not os.path.isdir(r'risultati_int\\'+tralicci):
            os.mkdir(r'risultati_int\\'+tralicci)
        if not os.path.isdir(r'risultati_int\\'+tralicci+"\\"+features):
            os.mkdir(r'risultati_int\\'+tralicci+"\\"+features)
        if not os.path.isdir(r'risultati_int\\'+tralicci+"\\"+features+"\\"+parametri):
            os.mkdir(r'risultati_int\\'+tralicci+"\\"+features+"\\"+parametri)
        
        pickle.dump({"YTest": YTest,
                     "YTrain": YTrain,
                     "XTest": XTest,
                     "XTrain": XTrain,
                     "X":X,
                     "Y":Y,
                     "path":path,
                     "int_predizione":globals.int_predizione,
                     "lasso":globals.lasso,
                     "span":globals.span,
                     "proporzione":globals.proporzione,
                     "soglia_bad_mincellv":globals.soglia_bad_mincellv,
                     "rapporto": globals.rapporto}, open(path+'dataset.pkl','wb'))
        
        
        
        
        
        
        
        # r'risultati_int\\t13008_t16399_t1059_t1021\\mincellvoltage_panelpower_soc_irradiation\\1_1_7_1_0.25\\dataset.pkl'
        