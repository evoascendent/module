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


pathDataOut = r'C:\Users\thch1015\Desktop\exodaten2020\daten\nochmal\Exotenhaus'

datePattern = '{:%Y%m%d%H}'
date = datePattern.format(datetime.today())


# Präfix zur Verifizierung von zip-Sensordaten im Ordner data2database
prefix = 'data'
# Dateiendung zur Verifizierung von zip-Sensordaten im Ordner data2database
ending = '.tar.gz'
# Präfix zur Verifizierung von dat-Sensordaten im Ordner data2database
dataPrefix = 'Id00124b'
# Dateiendung zur Verifizierung von dat-Sensordaten im Ordner data2database
dataEnding = '.dat'


# prüfe ob sich Dateteien im "Postausgangsordner" befinden
dataOutContent = os.listdir(pathDataOut)
# falls ja, gib mir die Namen aller .tar.gz mit entsprechendem Präfix als Liste
if len(dataOutContent) > 0:
    zipList = []
    dataList = []
    for file in dataOutContent:
        if file.endswith(ending) and (prefix in file):
            zipList.append(file)
    # Falls gezippte Daten vorhanden -> entpacken
    if len(zipList) > 0:
        # ergänze Dateinamen mit Pfaden
        unzipList = [os.path.join(pathDataOut, file) for file in zipList]
        # entpacke alle entsprechenden .ta.gz im aktuellen Ordner
        for file in unzipList:
            print('entpacke Datei: {}'.format(file))
            tar = tarfile.open(file)
            tar.extractall(pathDataOut)
            tar.close()
    # lese Ordnerinhalt des "Postausgangsordners" neu ein
    dataOutContent = os.listdir(pathDataOut)
    # erzeuge nun Liste aller .dat mit entsprechendem Präfix
    for file in dataOutContent:
        if file.endswith(dataEnding) and (dataPrefix in file):
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
                           save=False)
    print('Stapeln beendet...')

    print('Frameformat wird angepasst...')
    frame.exoFix2Frame()
    print('Anpassen beendet...')

    stopzeit = datetime.now()
    print('Stopzeit: {}'.format(stopzeit))
    delta = stopzeit - startzeit
    print('Es wurden {} Datensätze in {} verarbeitet.'.format(len(frame.frame),
          delta))

    frame.frame.sort_values('dateTime')
    frame.frame.reset_index(drop=True, inplace=True)

    # hier wird die absolute Luftfeuchtigkeit berechnet und angefügt
    frame.frame = cd.get_abs_hum(frame.frame)
