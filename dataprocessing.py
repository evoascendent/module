# -*- coding: utf-8 -*-
"""
Created on Wed May 31 13:34:54 2017

author: Christian Thiele
mail:   christian.thiele@live.de
datei: dataprocessing.py
version: 1.1.0
"""


import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy
import os


class Data2Frame:
    """Data2Frame erstellt einen Pandas-Dataframe mit der Bezeichnung 'frame'.
    ---------------------------------------------------------------------------
    Übergabeparameter: headerList = ["item1", "item2", "..."]

    Bei Aufruf ohne Übergabeparameter wird ein leerer Frame erzeugt.
    Um diesen zu füllen, muss erst per 'set_headerLine()' ein Header erzeugt
    und dann die Methode 'append_rows()' aufgerufen werden.
    """
    def __init__(self, headerList=None):
        self.headerLine = headerList
        self.frame = pd.DataFrame(columns=self.headerLine)

    def get_headerLine(self):
        """get_headerLine gibt den Header als Listenobjekt zurück
        """
        self.headerLine = self.frame.columns.values.tolist()
        return self.headerLine

    def set_headerLine(self, headerList):
        """Header setzen mit headerList = [("item1", "item2", "...")]
        """
        self.headerLine = headerList

    def append_rows(self, newRows):
        """neue Zeilen anhängen mit newRows = [((Zeile00, Zeile01),
                                                (Zeile10, Zeile11))]
        Spalten durch Komma getrennt, Zeilen in Klammern.
        Die Anzahl der Spaltenobjekte muss zur Anzahl der Headerobjekte passen.
        """
        appendix = pd.DataFrame(newRows, columns=self.headerLine)
        self.frame = self.frame.append(appendix, ignore_index=True)

    def drop_rows(self, rowIndices):
        """Die Zeilen mit den übergebenen Indices als
        rowIndices=[1, 2, 5, ..], werden gelöscht
        """
        self.frame.drop(self.frame.index[rowIndices], inplace=True)

    def drop_columns(self, columns):
        self.frame.drop(columns, 1, inplace=True)


class Data2FrameCSV(Data2Frame):
    """Data2FrameCSV erstellt einen Dataframe mit der Bezeichnung 'frame', wie
    die Basisklasse Data2Frame. Zusätzlich enthält sie Methoden zur Verarbeitung
    von CSV-Dateien.
    ---------------------------------------------------------------------------
    Übergabeparameter: headerList = [("item1", "item2", "...")]
                oder   fileName = "datei.csv", "datei.dat" oder "datei.txt"
                und    delim = "Trennzeichen"               (optional)
                       Header = Zeilenindex der Headerzeile (optional)
                       Encoding = "Zeichensatzkodierung"    (optional)

    Bei Aufruf ohne Übergabeparameter wird ein leerer Frame erzeugt.
    Um diesen zu füllen, muss erst per 'set_headerLine()' ein Header erzeugt
    und dann die Methode 'append_rows()' aufgerufen werden.
    """
    def __init__(self, headerList=None, fileName=None, delim=";", Header=0,
                 Encoding="utf8"):
        if fileName is None:
            super().__init__(headerList)
        else:
            self.name = fileName
            self.frame = pd.read_csv(self.name, sep=delim, header=Header,
                                     encoding=Encoding)

    def load_csv(self, fileName, delim=";", Header=0, Encoding="utf8"):
        """Falls ein leerer Frame vorliegt, kann eine csv-Datei geladen werden,
        um diesen zu füllen.
        -----------------------------------------------------------------------
        Übergabeparameter: fileName = "datei.csv", "datei.dat" oder "datei.txt"
                    und    delim = "Trennzeichen"               (optional)
                           Header = Zeilenindex der Headerzeile (optional)
                           Encoding = "Zeichensatzkodierung"    (optional)
        """
        self.name = fileName
        self.frame = pd.read_csv(self.name, sep=delim, header=Header,
                                 encoding=Encoding, skipinitialspace=True)

    def save_csv(self, fileName, delim=";", Header=True, index=False):
        """Speichert den Frame als csv-Datei mit ";" als Trennzeichen.
        -----------------------------------------------------------------------
        Übergabeparameter: fileName = "datei.csv", "datei.dat" oder "datei.txt"
                    und    delim = "Trennzeichen"                (optional)
                           Header = True, falls Header vorhanden (optional)
        andernfalls bitte: Header = False
                           index = True/False, Index wird gespeichert oder nicht
        """
        self.name = fileName
        self.frame.to_csv(self.name, sep=delim, header=Header, index=index)

    def append_csv(self, fileList, delim=";", Header=0,
                   Encoding="utf8"):
        """Stapelt beliebig viele csv-Dateien, welche den gleichen Header haben
        im Frame.
        -----------------------------------------------------------------------
        Übergabeparameter: fileList = ("datei1.txt", "datei2.txt", "...")
                           delim = "Trennzeichen"               (optional)
                           Header = Zeilenindex der Headerzeile (optional)
                           Encoding = "Zeichensatzkodierung"    (optional)
        """
        for i in range(len(fileList)):
            appendix = pd.read_csv(fileList[i], sep=delim, header=Header,
                                   encoding=Encoding)
            self.frame = self.frame.append(appendix, ignore_index=True)


class Data2FrameCSVP(Data2FrameCSV):
    """Data2FrameCSVP erstellt einen Dataframe mit der Bezeichnung 'frame', wie
    die Basisklasse Data2FrameCSV. Zusätzlich zu den Methoden zur Verarbeitung
    von CSV-Dateien enthält sie die Plotfunktionalität für den Temperaturversuch,
    die Fitfunktionalität und die Möglichkeit, die geplotteten Kurven als
    png-Datei abzuspeichern.
    ---------------------------------------------------------------------------
    Übergabeparameter: headerList = [("item1", "item2", "...")]
                oder   fileName = "datei.csv", "datei.dat" oder "datei.txt"
                und    delim = "Trennzeichen"               (optional)
                       Header = Zeilenindex der Headerzeile (optional)
                       Encoding = "Zeichensatzkodierung"    (optional)

    Bei Aufruf ohne Übergabeparameter wird ein leerer Frame erzeugt.
    Um diesen zu füllen, muss erst per 'set_headerLine()' ein Header erzeugt
    und dann die Methode 'append_rows()' aufgerufen werden.
    """
#    def __init__(self, headerList=None, fileName=None, delim=";", Header=0,
#                 Encoding="utf8"):
#        super().__init__(headerList, fileName, delim, Header, Encoding)

    def plot_curves(self, xAxis, curveList=None, function=None, funcYdata=None,
                    xLabel=None,
                    yLabel=None):
        """Es werden eine oder mehrere Kurven geplottet. Die Achsenbeschriftung
        wird aus den Spaltennamen übernommen oder kann übergeben werden.
        Für die y-Achse wird der Spaltenname der ersten Spalte aus der
        Kurvenliste verwendet.
        (sollte bei mehreren Kurven also angepasst werden)
        -----------------------------------------------------------------------
        Übergabeparameter: xAxis = "Spalte für x-Achsendaten"
                           curveList = (["Kurve1", "Kurve2", "..."])
                           xLabel = "x-Achsenbeschriftung" (optional)
                           yLabel = "y-Achsenbeschriftung" (optional)
                           function = Vorbereitung für Erweiterung
                           funcYdata = Vorbereitung für Erweiterung
        """

        if xLabel is None:
            xLabel = xAxis

        if yLabel is None:
            yLabel = curveList[0]

        self.fig = plt.figure()

        for i in range(len(curveList)):
            var = self.frame.groupby(xAxis)[curveList[i]].sum()
            var.plot(kind="line")
        # ToDo: legend
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.grid()
        plt.show()

    def save_figure(self, fileName=time.strftime("%Y_%m_%d_%H_%M")+".png"):
        """Speichert den Plot default als 'Zeitstempel.png' im aktuellen Ordner
        ab.
        -----------------------------------------------------------------------
        Übergabeparameter: filename = "/Pfad/zum/Zielordner/Dateiname.png"
        """
        self.fig.savefig(fileName)


class Exo2FrameCSVP(Data2FrameCSVP):
    '''Diese Klasse ist speziell für die Daten aus den Sensortags im Exotenhaus.
    '''
    def fix_timeStamp(self):
        '''Aus den Spalten 'date' und 'time', wird eine Spalte 'dateTime' erzeugt,
        welche einen Pandas-Timestamp enthält.
        '''
#        print(self.frame['date'])
        self.frame['time'] = self.frame['date'] + self.frame['time']
        # print(self.frame['time'])
#        self.frame['time'] = pd.to_datetime(self.frame['time'])
        self.drop_columns('date')
        self.frame.rename(columns={'time': 'dateTime'}, inplace=True)
        self.frame['dateTime'] = pd.to_datetime(self.frame['dateTime'],
                  format='%d.%m.%Y %H:%M:%S')
        # print(self.frame['dateTime'])

    def fix_empty(self):
        '''Löscht die leere, letzte Spalte.
        '''
        self.frame.drop('', 1, inplace=True)

    def fix_header(self):
        '''Entfernt die Leerzeichen aus den Spaltennamen.
        '''
        headerLine = self.get_headerLine()
        headerLineNew = [colNames.replace(' ', '') for colNames in headerLine]
        headerLineOldNew = zip(headerLine, headerLineNew)
        headerLineDict = dict(headerLineOldNew)
        self.frame.rename(columns=headerLineDict, inplace=True)

    def hexCol2int(self, column):
        self.frame[column] = self.frame[column].apply(lambda x: int(x, 16))

    def frame2numpyFloat(self):
        '''Wandelt die datetime-Objekte in epoch-Zeit und die ID in
        integer-Werte um, damit der Frame als numpy-Array ausgegeben
        werden kann.
        '''
        tempFrame = self.frame.copy()
        dateTime = tempFrame['dateTime']
        index = pd.DatetimeIndex(dateTime)
        epoch = index.astype(np.int64) // 10**9
        ID = tempFrame['ID'].apply(lambda x: int(x, 16))
        tempFrame['dateTime'] = epoch
        tempFrame['ID'] = ID
        numpyFloat = tempFrame.values
        return numpyFloat

    @staticmethod
    def removeString(frame, column, string):
        frame[column] = frame[column].apply(lambda x: x.replace(string, ''))
        # frame[column] = frame[column].apply(lambda x: x - prefix*100000)
        return frame

    def exoFix2Frame(self):
        '''Diese Funktion ist spezifisch für die derzeitige(21.11.2017)
        Formatierung der .dat-Dateien aus dem Exotenhaus angepasst. Es werden
        die Leerzeichen aus den Spaltennamen entfernt. Das überschüssige Prefix
        und das Leerzeichen aus 'ID' wird entfernt. Aus den Spalten 'date'
        und 'time' wird eine Spalte 'datetime' erzeugt und zuletzt werden leere
        Spalten entfernt.
        '''
        self.fix_header()
        # self.frame = Exo2FrameCSVP.removeString(self.frame, 'ID', '00124b')
        self.frame = Exo2FrameCSVP.removeString(self.frame, 'ID', ' ')
        self.fix_timeStamp()
        # self.hexCol2int(column='ID')
        self.fix_empty()

    @staticmethod
    def stackParty(fileList,
                   fileName=None,
                   Delimiter=';',
                   HeaderF=1,
                   HeaderL=1,
                   save=True,
                   saveName=None):
        '''Die Funktion hängt die Dateien aus 'fileList' an die Datei
        'fileName' an und gibt den Inhalt als Frame zurück.
        Falls fileName = None, wird aus allen Dateien in 'fileList'
        ein Frame erstellt. Der Frame wird als saveName exportiert.
        Falls der saveName nicht nicht übergeben wird,
        lautet er z.B. 'stacked201709111645.dat', im aktuellen Arbeitsordner.
        Ganz ohne Parameter passiert garnichts.
        Wichtig!
        Spezifizieren sie die Headerindizes, falls sich die Dateien zwischen denen,
        die angehangen werden un denen die sie anhängen wollen, unterscheiden!
        ---------------------------------------------------------------------------
        Übergabeparameter: fileName als '/Pfad/zur/Datei/fileName'
                           fileList als ['/Pfad/zur/Datei/fileName1', '..']
                           Delimiter als 'Trennzeichen'
                           HeaderF als Index für die Headerzeile falls fileName
                           HeaderL als Index für die Headerzeile fall fileList
        '''
        fileList_c = copy.deepcopy(fileList)
        if fileName is None:
            fileName = fileList_c[0]
            Header = HeaderL
            fileList_c.pop(0)
        else:
            Header = HeaderF
        tempFrame = Exo2FrameCSVP(fileName=fileName,
                                  delim=Delimiter,
                                  Header=Header)
        Header = HeaderL
        tempFrame.append_csv(fileList_c, Header=Header)
        stackedFrame = tempFrame

        if save is True:
            if saveName is None:
                saveName = 'stacked' + time.strftime('%Y%m%d%H%M') + '.dat'
            stackedFrame.save_csv(fileName=saveName)
        return stackedFrame
