# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 12:08:41 2022

@author: UTENTE
"""
#pip install tensorflow-probability
#pip install onnx-tf

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, LSTM, Softmax, Bidirectional
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from tensorflow.keras.optimizers import Adam
from keras.models import load_model
from keras.callbacks import ModelCheckpoint
from sklearn.metrics import accuracy_score
import onnx
from onnx_tf.backend import prepare

onnx_model = onnx.load("prova.onnx")
tf_rep = prepare(onnx_model)
tf_rep.export_graph("prova")
model = tf.keras.models.load_model('prova')

# with tf.gfile.GFile('prova.pb', "rb") as f:
#     graph_def = tf.GraphDef()
#     graph_def.ParseFromString(f.read())
# with tf.Graph().as_default() as graph:
#     tf.import_graph_def(graph_def, name='')