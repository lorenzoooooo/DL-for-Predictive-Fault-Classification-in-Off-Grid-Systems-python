# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 16:13:04 2022

@author: UTENTE
"""

import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
from datetime import date
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, LSTM, Bidirectional
# from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import StratifiedKFold
from tensorflow.keras.optimizers import Adam

''' load '''
dataset_path=r'C:\\Users\\UTENTE\\Desktop\\py\\risultati_int\\t13008_t16399_t1059_t1021\\mincellvoltage_panelpower\\1_1_1_3_0.25\\'
RESULT=pickle.load(open(dataset_path+'dataset.pkl','rb'))
X=RESULT['X']
Y=RESULT['Y']
path=RESULT['path']

''' baseline model'''
def create_baseline(numHiddenUnits, numClasses, lr):   
    initializer = tf.keras.initializers.GlorotNormal()
    model=Sequential()
    model.add(Bidirectional(LSTM(numHiddenUnits,
                                 activation='tanh',
                                 recurrent_activation='sigmoid',
                                 kernel_initializer=initializer,
                                 recurrent_initializer="orthogonal",
                                 unit_forget_bias=True,
                                 return_sequences=False)))      # input_shape=(len(XTrain[0]),inputSize),kernel_initializer=initializer
    model.add(Dense(numClasses,activation='sigmoid'))  
    model.add(Dense(1,activation='sigmoid'))
    adam = Adam(lr,epsilon = 1e-08)
    model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy','binary_crossentropy'])
    return model

''' parametri rete ''' 
lr=0.04
inputSize = 2
numHiddenUnits =15
numClasses = 2
maxEpochs = 12
miniBatchSize =10

''' folder in where to save'''
file=str(date.today().day) + '-' + str(date.today().month) + '_' + str(numHiddenUnits) + '_' + str(maxEpochs)+ '_' + str(lr)
if not os.path.isdir(dataset_path + "\\" + file):
    os.mkdir(dataset_path + "\\" + file)


''' Train '''
kf=4
n_runs=10
acc=[]

for z in range(n_runs):
    print('\n--- RUN %d / %d ---\n'% (z+1, n_runs))
    np.random.seed(z)
    # estimator = KerasClassifier(build_fn=create_baseline(numHiddenUnits, numClasses, lr), epochs=maxEpochs, batch_size=miniBatchSize, verbose=0)
    kfold = StratifiedKFold(n_splits=kf, shuffle=True, random_state=z)
    cvscores=[]
    for train, test in kfold.split(X, Y):
        model=create_baseline(numHiddenUnits, numClasses, lr) 
        model.fit(tf.gather(X,train), tf.gather(Y,train), epochs=maxEpochs, batch_size=miniBatchSize, verbose=0)
        scores = model.evaluate(tf.gather(X,test), tf.gather(Y,test), verbose=0)
        # print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
        cvscores.append(scores[1] * 100)
    print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))
    acc.append((np.mean(cvscores)))
acc_avg=np.mean(acc)
acc_std=np.std(acc)
print("total accuracy: %.2f%% (+/- %.2f%%)" % (acc_avg, acc_std))





