# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 15:39:43 2017
author: Esther Escribano Ortiz
mail:   escribanoesther@gmail.com
datei: datacalculation.py
version: 1.0.0
"""
import pandas as pd
import scipy.constants as const


class CalculateData:

    @staticmethod
    def get_abs_hum(frame, col_Humi="HDCHumi", col_Temp="HDCTemp",
                    single_col=False):
        '''
        <summary>
        Create a column in the frame with the ABSOLUTE HUMIDITY ['abs_Humi']
        calculated with frame data of the relative humidity and temperature
        <param name= frame
                     col_Humi (column name with relative humidity data)
                     col_Temp (column name with relative temperature data)
                     single_col (choose an option for return values)
        <returns>= optionA: frame with additional column for abs. humudity
                       optionB: frame with 3 columns['dateTime', 'ID',
                       'abs_Humi']
        '''
        frame = frame.copy()
        TempCelsius = frame[col_Temp]
        TempKelvin = TempCelsius + 273
        p_s = 6.1078 * 10 ** ((7.5 * TempCelsius)/(287.8 + TempCelsius))
        p_d = (frame[col_Humi]/100) * p_s
        M_H20 = 18.016  # M_H2O = 2 * hydrogen.mass + oxygen.mass
        frame['ABSHumi'] = round((100000 * M_H20 * p_d)/((const.R * 10 ** 3) * TempKelvin), 2)  # round(Zahl , 2) hinzugef. CT
        if single_col is False:
            return frame
        elif single_col is True:
            return frame[['dateTime', 'ID', 'ABSHumi']]

    @staticmethod
    def get_statistics(frame, statistics=['min', 'max', 'mean']):
        '''
        <summary>
        Calculate statistical data
        <param name= frame
                     statistics(list with statistics from describe method
                     to be calculated)
        <returns>= frame with statistics list as index,
                    eg.
                               Temperature  Humidity ...
                    min            75           74
                    max            85           83
                    mean           77           78
        '''
        stat_frame = pd.DataFrame()
        list_series = list()
        stat_frame = frame.describe()
        index_list = list(stat_frame.index)
        for stat in statistics:
            # get index number for statistical value: mean, max, etc.
            for i in (i for i, index in enumerate(index_list) if index is stat):
                series = stat_frame.iloc[i]
                list_series.append(series)
        final_frame = pd.DataFrame(list_series)
        return final_frame

    @staticmethod
    def get_stat_by_time(frame, columnTime='dateTime', period='H',
                         statistics='mean', indexTime=False):
        '''
        <summary>
        Calculate statistical data
        <param name= frame
                     column Time: colume with time/date
                     period = 'Y' (year), 'M' (month), 'W' (week),
                              'B' (business week), 'D' (calender day),
                              'H' (hourly) etc.
                     statistics= value to be calculated, e.g. 'mean', 'max',
                                 'min', 'count'...
                     Timestamp = False : if the type of the column is not of
                                 type Timestamp
        <returns>= frame with period column and statistical calculation in
                    further columns
                    eg. Mean values
                period           Temperature      Humidity
                    W1            25           74
                    W2            26           83
                    W3            27           78
        '''
        # overwrites original dataframe
        if not indexTime:
            frame=frame.copy()
            frame[columnTime] = pd.to_datetime(frame[columnTime])
        df = frame.set_index(columnTime)  # set Time column as index
        if statistics is 'mean':
            # resample by a period and calculate average
            df = df.resample(period).mean()
        elif statistics is 'max':
            # resample by a period and calculate maximum
            df = df.resample(period).max()
        elif statistics is 'min':
            # resample by a period and calculate minimum
            df = df.resample(period).min()
        elif statistics is 'count':
            # resample by a period and calculate count
            df = df.resample(period).count()
        else:
            print('Statistical value not found.')
        return df  # return frame with date as index

## pivot table --> USING numpy why functions , mean is default
#    df.pivot_table(index='ID', columns='dateTime', aggfunc='mean',
#                   margins=True)  # margins = shows average in All column
##               Humi        Temp        All     Humi         Temp       All
##  dateTime   05/2/2017  05/2/2017  05/2/2017  05/2/2017  05/2/2017  05/2/2017
##    ID
##    7874545454    44       42           41      42            45        43
##    7575757554    49       45           48      48            47        47
#
#    df.pivot_table(index=pd.Grouper(freq='M', key='dateTime',
#                                    columns='HDCHumi'))



                    ##### Statistics      ############
#            dfStat = CalculateData.get_statistics(frame)
#            min_val = dfStat[yAxis[0]].iloc[0]
#            max_val = dfStat[yAxis[0]].iloc[1]
#            mean_val = dfStat[yAxis[0]].iloc[2]
