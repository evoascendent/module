# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 21:52:35 2018

@author: thch1015
"""

import os
import tarfile
import argparse
import time
from datetime import datetime
from dataprocessing import Exo2FrameCSVP as d2f
from datacalculation import CalculateData as cd
from shutil import copyfile
import dbTools as db


# pathDataOut = r'D:\Benutzer\thch1015\nextcloud\HSKA\Hiwi\HiWiWS1920\Projekte\AuswertungenZoo\Elefanten\tar_2020\acc_gyro\b03'
# pathDataOut = r'D:\Benutzer\thch1015\nextcloud\HSKA\Hiwi\HiWiWS1920\Projekte\AuswertungenZoo\Elefanten\tar_2020\battery\b03'
pathDataOut = r'E:\nextcloud\HSKA\Hiwi\HiWiWS1920\Projekte\AuswertungenZoo\Flamingos\Daten_2019_Flamingos\acc_gyro\ece4'

# saveName = 'ece4temp.dat'
# saveName = '06c6temp.dat'
# saveName = '6985temp.dat'
# saveName = '7c83temp.dat'
# saveName = 'fb86temp.dat'

saveName = 'ece4acc.dat'
# saveName = '06c6acc.dat'
# saveName = '6985acc.dat'
# saveName = '7c83acc.dat'
# saveName = 'fb86acc.dat'

# prüfe ob sich Dateteien im "Postausgangsordner" befinden
dataOutContent = os.listdir(pathDataOut)
# falls ja, gib mir die Namen aller .tar.gz mit entsprechendem Präfix als Liste
if len(dataOutContent) > 0:
    dataList = []
    # erzeuge nun Liste aller .dat mit entsprechendem Präfix
    for file in dataOutContent:
        dataList.append(file)
    # fall diese Liste mehr als 0 Elemente enthält, sind neue Daten vorhanden
    if len(dataList) > 0:
        NEW_DATA = True
    else:
        NEW_DATA = False
else:
    NEW_DATA = False

# Falls neue Sensordaten vorhanden, werden diese gestapelt zu einer .dat-Datei
if NEW_DATA is True:
    startzeit = datetime.now()
    print('Startzeit: {}'.format(startzeit))
    stackList = [os.path.join(pathDataOut, file) for file in dataList]
    print('Dateien werden gestapelt...')
    frame = d2f.stackParty(fileList=stackList,
                           HeaderF=1,
                           HeaderL=1,
                           save=True,
                           saveName=saveName)
    print('Stapeln beendet...')

    stopzeit = datetime.now()
    print('Stopzeit: {}'.format(stopzeit))
    delta = stopzeit - startzeit
    print('Es wurden {} Datensätze in {} verarbeitet.'.format(len(frame.frame),
          delta))

