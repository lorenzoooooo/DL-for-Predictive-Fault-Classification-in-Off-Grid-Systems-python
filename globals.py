# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 11:01:09 2022

@author: UTENTE
"""
''' global variables'''
## inserisco i parametri
# lasso è a durata in giorni della sequenza, span è l'intervallo tra una
# sequenza e l'altra e int_predizione è l'intervallo predittivo in giorni.
# proporzione è il rapporto tra sequenze patologiche e sane nel dataset (se
# è 2 allora avrò che per ogni sequenza patologica ne ho due sane).  Rapporto è solo per il caso
# di partizione statica del dataset ed è la ercentuale di sequenze nel Ts set rispetto al Tr set
# Torre è l'id della torre, name dice se la l'apparato contiene la stazione 
# meteo o meno e tipo differenzia tra digil pura e digil_iotbox
# global tipo, name, torre 
def initialize():
    global lasso, span, int_predizione, soglia_bad_mincellv, proporzione, rapporto
    lasso=3
    span=1
    int_predizione=7
    proporzione=3         
    soglia_bad_mincellv=3200
    rapporto=0.25