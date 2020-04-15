# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 16:35:43 2017
author: Esther Escribano Ortiz
mail:   escribanoesther@gmail.com
datei: datacontinuity.py
version: 1.0.0
"""
import pandas as pd
import numpy as np

rng = pd.date_range('1/1/2011', periods=72, freq='H')


class Continuity:

    # index from frame has to be time- shows only if no data at all
    @staticmethod
    def get_missing_time(frame, startCnt='01-01-2017', endCnt='01-11-2017',
                         freqCnt='D', columnTime='dateTime', indexTime=False):
        '''
        <summary>
            Overview over missing data over a period of time
            <param name= frame
                         startCnt: start date
                         endCnt: stop date
                         freqCnt: frequency of missing data, e.g. 'D' for day, 'H' for hour
                         columnTime: name of the time column
                         indexTime: = False if Dataframe index is not a date
            <returns>= list with missing dates
        '''
        daily_index = pd.date_range(start=startCnt, end=endCnt, freq=freqCnt)
        if not indexTime:
            frame[columnTime] = pd.to_datetime(frame[columnTime])
            df = frame.set_index(columnTime)
            difference = daily_index.difference(df.index)
        else:
            difference = daily_index.difference(frame.index)
        return difference

    @staticmethod
    def delete_data(frame, column='HDCTemp', min_val=0., max_val=35):
        '''
        <summary>
            Delete non correct data
            <param name= frame
                         column: column to be corrected
                         min_val: value under or equal to this will be replaced 
                                 with NaN
                         max_val: value over or equal to this will be replaced 
                                 with NaN
            <returns>= frame with corrected values
                        eg. 
                    dateTime                HDCTemp      HDCHumi
                    01.02.2018 00:00:00     np.NaN          83
                    01.02.2018 00:00:01          25         85
                    01.02.2018 00:00:02          24         78
        '''
        frame = frame.copy()
        frame[column] = np.where(frame[column]>=max_val, np.nan, frame[column])
        frame[column] = np.where(frame[column]<=min_val, np.nan, frame[column])
        return frame
        #        frame[column].replace(to_replace=[min_val, max_val], value=np.nan, inplace=True)
        
    #    # frame shall have time as index
#    new_frame = frame.interpolate(method='time')
#    new_frame1 = frame.dropna()  # any value in row NaN
#    new_frame2 = frame.dropna(how='all')  # value in all raws missing
#    new_frame3 = frame.dropna(thresh=2)  # at least 2 valid values
#    new_frame4 = frame.replace([-99999,-8888], np.Nan)
#    new_frame5 = frame.replace({'temp':-99999,'humi':-99999}, np.Nan)  
#    # replace value of a specific column
#    new_frame6 = frame.replace({-99999: np.NaN,'something':'other'})  
#    new_frame7 = frame.replace({'temp':['A-Za-z']}, '',regex=True) 
#    # replace anything that is part of an alphabet with a blanc space
#    new_frame8 = frame.replace(['something', 'otherthing'][1,2])
#    # replace value something with 1, other thing with 2, etc
#    dt = pd.date_range(start='01-01-2017', end='01-10-2017', freq='D')
#    idx = pd.DatetimeIndex(dt)
#    df.reindex(idx, inplace=True)  # replace index and replace frame
#    