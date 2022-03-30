# from numpy.random import seed
# seed(1)
# from tensorflow.random import set_seed
# set_seed(2)

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 16:40:30 2022

@author: UTENTE
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
from datetime import date
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, LSTM, Softmax, Bidirectional


from tensorflow.keras.optimizers import Adam
# from tensorflow.keras.optimizers.schedules import PiecewiseConstantDecay
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
from sklearn.metrics import accuracy_score
# from keras.callbacks import LearningRateScheduler
# import math

 
# ''' learning rate schedule '''
# def step_decay(epoch,lr):
#     drop = 0.5
#     epochs_drop = round(epoch/5)
#     lrate = lr * math.pow(drop, math.floor((1+epoch)/epochs_drop))
#     return lrate


''' load '''
dataset_path=r'C:\\Users\\UTENTE\\Desktop\\py\\risultati_int\\t13008_t16399_t1059_t1021\\mincellvoltage_panelpower\\1_1_3_3_0.25\\'
RESULT=pickle.load(open(dataset_path+'dataset.pkl','rb'))
XTrain=RESULT['XTrain']
YTrain=RESULT['YTrain']
XTest=RESULT['XTest']
YTest=RESULT['YTest']
path=RESULT['path']

''' check '''
# plt.figure
# d=random.randint(0,len(XTrain))
# plt.plot(XTrain[d])
# xlabel("Time Step")
# title(strcat("Training Observation ",string(YTrain(d))));
# numFeatures = size(XTrain{1},1);
# legend("Feature " + string(1:numFeatures),'Location','northeastoutside')

''' parametri rete ''' 
inputSize = 2
numHiddenUnits =15
numClasses = 2
maxEpochs = 10
miniBatchSize =22
lr=0.04

''' folder in where to save'''
file=str(date.today().day) + '-' + str(date.today().month) + '_' + str(numHiddenUnits) + '_' + str(maxEpochs)+ '_' + str(lr)
if not os.path.isdir(dataset_path + "\\" + file):
    os.mkdir(dataset_path + "\\" + file)

''' definizione della rete'''
initializer = tf.keras.initializers.GlorotNormal()
model=Sequential()
model.add(Bidirectional(LSTM(numHiddenUnits,
                             return_sequences=False, kernel_initializer=initializer)))      # input_shape=(len(XTrain[0]),inputSize),kernel_initializer=initializer
model.add(Dense(numClasses))
# model.add(Softmax())
model.build([len(XTrain),len(XTrain[0]),inputSize])
model.summary()

''' Settings '''
# step = tf.Variable(lr/2, trainable=False)
# boundaries = list(range(2*round(len(XTrain)/maxEpochs), len(XTrain), 2*round(len(XTrain)/maxEpochs)))
# values = [lr, lr/2, lr/4, lr/8, lr/16]
# learning_rate_fn = PiecewiseConstantDecay(boundaries, values)
# adam = Adam(learning_rate_fn(step),epsilon = 1e-08)
adam = Adam(lr,epsilon = 1e-08)
# chk = ModelCheckpoint(filepath=dataset_path + file, monitor='accuracy',
                      # save_best_only=True, mode='max', verbose=1)
model.compile(loss='binary_crossentropy', optimizer=adam, metrics=['accuracy', 'binary_crossentropy'])
# lrate = LearningRateScheduler(step_decay(maxEpochs, lr))
# callbacks_list = [lrate]

''' Train '''
history=model.fit(XTrain, YTrain, 
          epochs=maxEpochs, batch_size=miniBatchSize, shuffle=True, verbose=2) #callbacks=[chk]

''' plot '''
fig, axs = plt.subplots(2)
fig.suptitle('Metrics')
axs[0].plot(history.history['accuracy'])
axs[0].set_title('accuracy')
axs[1].plot(history.history['binary_crossentropy'])
axs[1].set_title('binary_crossentropy')
# plt.figure()
# plt.plot(history.history['accuracy'])
# plt.plot(history.history['binary_crossentropy'])

''' Test '''
YPred=list()
# model.load_weights(dataset_path + file)
probpred = model.predict(XTest)
YPred=np.argmax(probpred,axis=1)
acc=accuracy_score(YTest, YPred)
print('accuracy:', acc)


# round(acc,2)
# +'_'+options.LearnRateDropFactor+'_piecewise_'+ options.Shuffle





