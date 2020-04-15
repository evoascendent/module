# -*- coding: utf-8 -*-
"""
Created on Fri Dec 1 16:35:43 2017
author: Esther Escribano Ortiz
mail:   escribanoesther@gmail.com
datei: dataplotting.py
version: 1.0.0
"""
from dataselection import SelectData
from datacalculation import CalculateData
from datacontinuity import Continuity
# python official
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib.dates import AutoDateLocator

import numpy as np

dpi = 80
figsize = (12, 7)


class PlotData:

    global dpi
    global figsize

    @staticmethod
    def Exo_per_selection(frame,
                          plot_liste_selection=['oben', 'mitte', 'unten'],
                          plot_title=['Temperature - oben',
                                      'Temperature - mitte',
                                      'Temperature - unten'],
                          plot_xAxis='dateTime', plot_yAxis='HDCTemp',
                          plot_xlabel='dateTime', plot_ylabel="HDCTemp/ C",
                          plot_time=False,
                          plot_fig=['Oben_Temp.png', 'mitte_Temp.png',
                                    'unten_Temp.png'],
                          plot_color=['darkblue', 'orange', 'green'],
                          plot_sel='Level'):
        '''
        <summary>
            Plot functionality for exodaten
            <param name= frame
                         plot_liste_selection: list with data to be plotted
                         plot_title: list with title for plots* 
                         plot_xAxis: string (column name) xAxis for plot
                         plot_yAxis: string (column name) yAxis for plot
                         plot_xlabel: string for label for x Axis
                         plot_ylabel: string for label for y Axis
                         plot_time: bool = True if time selection necessary
                         plot_fig: list with names for files*
                         plot_color: list with color for plots*
                         plot_sel: column name for plot
                         *(list shall have the same amount of entries as the list of plot_liste_selection)                         
            <returns>= no return -
                    -> plot of 3 figures: one per category of plot_liste_selection             
        '''
        # dictionary fuer Plot-Titel
        plot_titledict = dict(zip(plot_liste_selection, plot_title))
        # dictionary fuer Plot-Name (zum Speichern)
        plot_figdict = dict(zip(plot_liste_selection, plot_fig))
        # dictionary fuer Plot-Farbe
        plot_colordict = dict(zip(plot_liste_selection, plot_color))
        # Dataframe pro 'Ebene'
        print("Dataframe pro Ebene")
        for ebene in plot_liste_selection:
            print(ebene, plot_liste_selection)
            df = SelectData.select_data(frame, column=plot_sel, 
                                        time=plot_time,
                                        filtervalue=[ebene])
            cal = pd.DataFrame()
            cal = CalculateData.get_statistics(df)
            # Listen zum Plotten
            x_, y_ = SelectData.get_list_plot(df, columnx=plot_xAxis,
                                              columny=plot_yAxis)
        ##### Plotten           ############
            fig = plt.figure(dpi=dpi, figsize=figsize)
            ax = fig.add_subplot(1, 1, 1)
            color = plot_colordict[ebene]
            ax.plot(x_, y_, '.', color=color, label=ebene, markersize=1)
            minval = cal[plot_yAxis][0]
            maxval = cal[plot_yAxis][1]
            title1 = plot_titledict[ebene] + ' min: ' + str(minval) + ' max: '+ str(maxval)
            ax.set_title(title1, fontsize=15)
            ax.set_xlabel(plot_xAxis)
            ax.set_ylabel(plot_ylabel)
            xFmt = md.DateFormatter('%d.%m.%y')  # '%d.%m.%y_%H:%M'
#          xlocator = md.HourLocator(byhour=range(24), interval=24)
#          ax.xaxis.set_major_locator(xlocator)
            xloc = plt.MaxNLocator(28)
            ax.xaxis.set_major_locator(xloc)
            ax.xaxis.set_major_formatter(xFmt)
            plt.xticks(rotation=45)
            ax.legend(loc='best')
            plt.grid(True)
            plt.show()
            figname1 = plot_figdict[ebene]
            fig.savefig(figname1, bbox_inches='tight')
            print("plot saved ", figname1)

    @staticmethod
    def Exo_selection(frame,
                      plot_liste_selection=['oben', 'mitte', 'unten'],
                      plot_title='Temperature - per Level',
                      plot_xAxis='dateTime', plot_yAxis='HDCTemp',
                      plot_xlabel='dateTime', plot_ylabel='HDCTemp / C',
                      plot_time=False,
                      plot_figname='TempPerLevel.png',
                      plot_color=['darkblue', 'orange', 'green'],
                      plot_sel='Level'):
        '''
        <summary>
         Plot functionality for exodaten
            <param name= frame
                         plot_liste_selection: list with data to be plotted
                         plot_title: title of plot
                         plot_xAxis: string (column name) xAxis for plot
                         plot_yAxis: string (column name) yAxis for plot
                         plot_xlabel: string for label for x Axis
                         plot_ylabel: string for label for y Axis
                         plot_time: bool = True if time selection necessary
                         plot_figname: string with file name
                         plot_color: list with color for plots from plot_liste_selection
                         plot_sel: column name for plot                         
            <returns>= no return -
                    -> plot of 1 figures: all categories from plot_liste_selection in one plot
        '''
        # dictionary fuer Plot-Farbe
        plot_colordict = dict(zip(plot_liste_selection, plot_color))
        # Dataframe pro 'ebene'
        fig = plt.figure(dpi=dpi, figsize=figsize)
        ax = fig.add_subplot(1, 1, 1)
        for ebene in plot_liste_selection:
            print(ebene, plot_liste_selection)
            color = plot_colordict[ebene]
            df = SelectData.select_data(frame, column=plot_sel,
                                        time=plot_time, filtervalue=[ebene])
            # Listen zum Plotten
            x_, y_ = SelectData.get_list_plot(df, columnx=plot_xAxis,
                                              columny=plot_yAxis)
        ##### Plotten           ############
            ax.plot(x_, y_, '.', color=color, label=ebene, markersize=1)
        ax.set_title(plot_title, fontsize=15)
        ax.set_xlabel(plot_xlabel)
        ax.set_ylabel(plot_ylabel)
        xFmt = md.DateFormatter('%d.%m.%y')  # '%d.%m.%y_%H:%M'
#        xlocator = md.HourLocator(byhour=range(24), interval=24)
#        ax.xaxis.set_major_locator(xlocator)
        xloc = plt.MaxNLocator(28)
        ax.xaxis.set_major_locator(xloc)
        ax.xaxis.set_major_formatter(xFmt)
        plt.xticks(rotation=45)
        ax.legend(loc='best')
        plt.grid(True)
        plt.show()
        fig.savefig(plot_figname, bbox_inches='tight')
        print("plot saved ", plot_figname)

    @staticmethod
    def Exo_stat_selection(frame,
                           plot_liste_selection=['oben', 'mitte', 'unten'],
                           plot_title='Temperature - average - per Level',
                           plot_stat='mean', plot_stat_period='H',
                           plot_indexTime=False,
                           plot_xAxis='dateTime', plot_yAxis='HDCTemp',
                           plot_xlabel='dateTime', plot_ylabel='HDCTemp / C',
                           plot_sel='Level', plot_time=False,
                           plot_columny='HDCTemp', plot_columnx=None,
                           plot_TimeX=True, plot_IndexTime=True,
                           plot_color=['darkblue', 'orange', 'green'],
                           plot_figname='TempAvgPerLevel.png'):
        '''
        <summary>
         Plot functionality for exodaten
            <param name= frame
                         plot_liste_selection: list with data to be plotted
                         plot_title: title of plot
                         plot_stat: statistical value requested 'mean', 'min',...
                         plot_stat_period= statistical value per hour, day, etc. 
                         plot_xAxis: string (column name) xAxis for plot
                         plot_yAxis: string (column name) yAxis for plot
                         plot_xlabel: string for label for x Axis
                         plot_ylabel: string for label for y Axis
                         plot_time: bool = True if time selection necessary
                         plot_figname: string with file name
                         plot_color: list with color for plots from plot_liste_selection
                         plot_columny:
                         plot_columnx:
                         plot_TimeX:
                         plot_IndexTime:
                         plot_color: list with color for plots from plot_liste_selection
                         plot_sel: column name for plot                         
            <returns>= no return -
                    -> plot of 1 figures: statistical values from all 
                    categories from plot_liste_selection in one plot
        '''
        # dictionary fuer Plot-Farbe
        plot_colordict = dict(zip(plot_liste_selection, plot_color))
        # Dataframe pro Ebene
        fig = plt.figure(dpi=dpi, figsize=figsize)
        ax = fig.add_subplot(1, 1, 1)
        for ebene in plot_liste_selection:
            print(ebene, plot_liste_selection)
            color = plot_colordict[ebene]
            df = SelectData.select_data(frame, column=plot_sel,
                                        time=plot_time, filtervalue=[ebene])
        ##### Statistics      ############
            dfStat = CalculateData.get_stat_by_time(df,
                                                    columnTime=plot_xAxis,
                                                    period=plot_stat_period,
                                                    statistics=plot_stat,
                                                    indexTime=plot_indexTime)
            x_, y_ = SelectData.get_list_plot(dfStat, columny=plot_columny,
                                              columnx=plot_columnx,
                                              TimeX=plot_TimeX,
                                              IndexTime=plot_IndexTime)
        ##### Plotten           ############
            ax.plot(x_, y_, '-', color=color, label=ebene)
#        times = pd.date_range('2017-11-01', periods=30)
        fig.autofmt_xdate()
        ax.set_title(plot_title, fontsize=15)
        ax.set_xlabel(plot_xlabel)
        ax.set_ylabel(plot_ylabel)
        xFmt = md.DateFormatter('%d.%m.%y')
#        xlocator = md.HourLocator(byhour=range(24), interval=24)
#        ax.xaxis.set_major_locator(xlocator)
        xloc = plt.MaxNLocator(28)
        ax.xaxis.set_major_locator(xloc)
        ax.xaxis.set_major_formatter(xFmt)
        plt.xticks(rotation=45)
#        plt.xticks(times.to_pydatetime())
        ax.legend(loc='best')
        plt.grid(True)
        plt.show()
        fig.savefig(plot_figname, bbox_inches='tight')
        print("plot saved ", plot_figname)
        
    @staticmethod
    def define_name(my_list=['oben', 'mitte', 'unten'],
                    string='Temperature', figname=True, data_end='.png'):
        '''
        <summary>
         Plot functionality for exodaten
            <param name= my_list: name of list
                         string: name to be attached to list
                         figname: if list of name shall be generated for a file
                         data_end: ending of data file, e.g. png, jpg, etc. 
            <returns>= list with definded names
        '''
        if figname:
            my_new_list = [string + '_' + x + data_end for x in my_list]
        else:
            my_new_list = [string + ' ' + x for x in my_list]

        return my_new_list

# pending all: - figsize, DateFormatter, xlocator -> by hour?