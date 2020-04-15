# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 15:41:06 2018

@author: thch1015
"""
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import numpy as np
import pandas as pd
import os
import math


class FitFunctions:
    '''
    Funtions for scipy.optimize.curve_fit
    '''
    def __init__(self):
        pass

    @staticmethod
    def pt1(t, tau, K, t0, A):
        # tau       Zeitkonstante
        # K         Proportionalanteil
        # t0        Startzeitpunkt
        # A         Anfangswert (bei t = t0)
        y = K * (1 - np.exp(-(t - t0) / tau))
        # Fuer t < t0 muss y den Anfangswert A annehmen
        # Die y-Werte werden daher mit dem Faktor (1-Fermifunktion) gewichtet
        y = y * (1.0 - FitFunctions.fermi(t, t0, 0.1)) + A
        return y

    @staticmethod
    def pt2(t, tau1, tau2, K, t0, A):
        y = K * (1 - (1/(tau1-tau2))*(tau1*np.exp(-(t-t0)/tau1)-tau2*np.exp(-(t-t0)/tau2)))
        y = y * (1.0 - FitFunctions.fermi(t, t0, 0.1)) + A
        return y

    @staticmethod
    def linear(x, m, c):
        y = m * x + c
        return y

    @staticmethod
    def circle(r, x0, y0, n):
        theta = np.linspace(0., 2. * np.pi, n, endpoint=False)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        return x0 + x, y0 + y

    @staticmethod
    def sinc(x, k, l, m):
        y = k * np.sin(l * x) / m * x
        return y

    @staticmethod
    def fermi(t, t0, eps):
        f = 1.0 / (1.0 + np.exp((t - t0) / eps))
        return f

    @staticmethod
    def exp(x, a, b, c):
        return a * np.exp(b*x) + c
    
    @staticmethod   
    def sigmoid_s(x, a, b):
        return 1 / (1 + np.exp(-b*(x-a)))
    
    @staticmethod
    def sigmoid(x, L, x0, k, b):
        return L / (1 + np.exp(-k*(x-x0))) + b

#******************************************************************************
# useful stuff
#******************************************************************************

# für Cassandra
def pandas_factory(colnames, rows):
    return pd.DataFrame(rows, columns=colnames)


# Ordner- und Dateioperationen*************************************************

def search(path, ending):
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(ending):
                yield os.path.join(root, filename)


def search2(path, extension):
    """
       extension with leading point, for example: ".png"
    """
    for root, dirs, filenames in os.walk(path):
        for filename in filenames:
            if os.path.splitext(filename)[-1] == extension:
                yield os.path.join(root, filename)


# Mathe************************************************************************
def ggT(a, b):
    if a == 0:
        ggT = abs(b)
    elif b == 0:
        ggT = abs(a)
    else:
        if b > a:
            a, b = b, a
        while True:
            h = a % b
            a = b
            b = h
            if b == 0:
                ggT = abs(a)
                break
    return ggT


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    '''rel_tol ist eine relative Toleranz, sie wird mit der größeren der beiden
    Argumente multipliziert; Wenn die Werte größer werden, nimmt auch die
    zulässige Differenz zwischen ihnen zu, während sie immer noch als gleich
    angesehen werden.
    abs_tol ist eine absolute Toleranz, die in allen Fällen abs_tol angewendet
    wird. Wenn die Differenz kleiner als eine dieser Toleranzen ist, werden die
    Werte als gleich angesehen.
    '''
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


# Elektrotechnik****************************************************************

def adc2voltage(adcValue, resolution, referenceMillivolt):
    bits = pow(2, resolution-1)
    voltageMillivolt = (adcValue * referenceMillivolt)/bits
    return voltageMillivolt


# GUI***************************************************************************

def questionbox(self, question=None, yesFunction=None, noFunction=None):
    if question is not None:
        reply = QMessageBox.question(self, 'Achtung', question,
                                     QMessageBox.Yes |
                                     QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            if yesFunction is not None:
                yesFunction()
            else:
                pass
        else:
            if noFunction is not None:
                noFunction()
            else:
                pass
    else:
        pass


def errorbox(message):
    box = QMessageBox()
    box.setIcon(QMessageBox.Critical)
    box.setWindowTitle('Achtung!')
    box.setText(message)
    box.setStandardButtons(QMessageBox.Ok)
    box.exec()


def warningbox(message):
    box = QMessageBox()
    box.setIcon(QMessageBox.Warning)
    box.setWindowTitle('Warnung!')
    box.setText(message)
    box.setStandardButtons(QMessageBox.Ok)
    box.exec()


def infobox(message):
    box = QMessageBox()
    box.setIcon(QMessageBox.Information)
    box.setWindowTitle('Information!')
    box.setText(message)
    box.setStandardButtons(QMessageBox.Ok)
    box.exec()


def fDialog():
    box = QFileDialog()
    box.setFileMode(QFileDialog.ExistingFile)
    box.setAcceptMode(QFileDialog.AcceptOpen)
    fileNameTemp = box.getOpenFileName()
    if len(fileNameTemp[0]) > 5:  # Wie geht das allgemeiner?
        fileName = fileNameTemp[0]
    else:
        fileName = None
    # print(fileName)
    return fileName


"""
Bezeichnungen:
r = relative Luftfeuchte
T = Temperatur in °C
TK = Temperatur in Kelvin (TK = T + 273.15)
TD = Taupunkttemperatur in °C
DD = Dampfdruck in hPa
SDD = Sättigungsdampfdruck in hPa

Parameter:
a = 7.5, b = 237.3 für T >= 0
a = 7.6, b = 240.7 für T < 0 über Wasser (Taupunkt)
a = 9.5, b = 265.5 für T < 0 über Eis (Frostpunkt)

R* = 8314.3 J/(kmol*K) (universelle Gaskonstante)
mw = 18.016 kg/kmol (Molekulargewicht des Wasserdampfes)
AF = absolute Feuchte in g Wasserdampf pro m3 Luft

Formeln:
SDD(T) = 6.1078 * 10^((a*T)/(b+T))
DD(r,T) = r/100 * SDD(T)
r(T,TD) = 100 * SDD(TD) / SDD(T)
TD(r,T) = b*v/(a-v) mit v(r,T) = log10(DD(r,T)/6.1078)
AF(r,TK) = 10^5 * mw/R* * DD(r,T)/TK; AF(TD,TK) = 10^5 * mw/R* * SDD(TD)/TK
"""

def getDewPoint(humRel, humTemp):
    if humTemp >= 0:
        a = 7.5
        b = 237.3
    else:
        a = 7.6
        b = 240.7

    SDD = 6.1078 * 10**((a * humTemp) / (b + humTemp))
    DD = humRel / 100 * SDD
    v = math.log10(DD / 6.1078)
    humDP = b * v / (a - v)
    return round(humDP, 2)
