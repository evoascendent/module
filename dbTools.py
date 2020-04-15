# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 10:44:49 2018

@author: thch1015
"""

# from cassandra.cluster import Cluster
# from cassandra.auth import PlainTextAuthProvider
import pandas as pd
import toolsCT as tools
import queriesCT as qu
import paramiko
import sqlite3
import sqlalchemy as sa
import os


# =============================================================================
# class Casspi:
#     def __init__(self, user, password):
#         self.user = user
#         self.password = password
#         self.ipList = ['192.168.178.10',
#                        '192.168.178.20',
#                        '192.168.178.30',
#                        '192.168.178.40',
#                        '192.168.178.50',
#                        '192.168.178.60',
#                        '192.168.178.70',
#                        '192.168.178.80']
#         self.casspi, self. session = self.connect()
#         self.keyspace = 'exoten'
#         self.table = 'exodaten'
# 
#     def connect(self):
#         credentials = PlainTextAuthProvider(username=self.user, password=self.password)
#         casspi = Cluster(self.ipList, auth_provider=credentials)
#         session = casspi.connect()
#         session.row_factory = tools.pandas_factory
#         session.default_fetch_size = None
#         print('got connection to casspi-cluster...')
#         return casspi, session
# 
#     def createKsTbl(self, ksName, tblName):
#         self.keyspace = ksName
#         self.table = tblName
#         queryKeyspace = qu.Casspi.queryCreateKeyspaceNTS33
#         queryTable = qu.Casspi.queryCreateTableExo
#         self.session.execute(queryKeyspace % self.keyspace, timeout=None)
#         self.session.execute(queryTable.format(self.keyspace, self.table), timeout=None)
#         print('created keyspace {} and table {}...'.format(self.keyspace, self.table))
# 
#     def createIdx(self, col='id'):
#         secIdxCol = col
#         queryIdx = qu.Casspi.queryCreateIdx
#         self.session.execute(queryIdx.format(self.keyspace, self.table, secIdxCol), timeout=None)
# 
#     def insertDat(self, dataFile):
#         queryInsert = qu.Casspi.queryInsertExoAll
#         headerLine = ['datetime',
#                       'id',
#                       'batvolt',
#                       'rssi',
#                       'seq',
#                       'uptime',
#                       'objtemp',
#                       'airpres',
#                       'hdchumi',
#                       'hdctemp',
#                       'ambtemp',
#                       'amblight']
#         dataframe = pd.read_csv(dataFile, sep=';',
#                                 header=0)
#         dataframe.dropna(inplace=True)
#         dataframe.reset_index(drop=True, inplace=True)
#         dataframe['dateTime'] = pd.to_datetime(dataframe['dateTime'])
#         print('Datei eingelesen...\nStarte Übertragung...')
#         counter = 0
#         for row in dataframe.itertuples():
#             counter += 1
#             print('Zeile: {}'.format(row[1]))
#             headerLineValues = zip(headerLine, row)
#             insertionDict = dict(headerLineValues)
#             insertionDict['day'] = insertionDict['datetime'].strftime('%Y-%m-%d')
#             insertionDict['month'] = insertionDict['datetime'].strftime('%Y-%m')
#             insertionDict['datetime'] = insertionDict['datetime'].strftime('%Y-%m-%d %H:%M:%S')
#             self.session.execute(queryInsert.format(self.keyspace, self.table), insertionDict, timeout=None)
#             # print(insertionDict)
#             if counter % 1000 == 0:
#                 print('{} Zeilen übertragen...'.format(counter))
#         print('Alle Daten nach {}.{} übertragen!'.format(self.keyspace, self.table))
# 
#         limit = '5'
#         query = """select * from {}.{}""".format(self.keyspace, self.table, limit)
#         result = self.session.execute(query, timeout=None)
#         frame = result._current_rows
#         print('Datenauszug (die ersten {} Zeilen):\n{}'.format(limit, frame))
# 
#     def getDataDayInterval(self, day=None, start=None, end=None, colList=None, idList=None):
#         pass
# 
#     def getDataMonthInterval(self, month=None, start=None, end=None, colList=None, idList=None):
#         pass
# 
#     def getDataDatetimeInterval(self, start=None, end=None, colList=None, idList=None):
#         pass
# 
#     @staticmethod
#     def exo2cassandra():
#         pass
# 
#     def shutdown(self):
#         self.casspi.shutdown()
#         print('Die Verbindung wurde geschlossen!')
# 
# 
# class ClusterHW:
#     casspiIP = ['192.168.178.10',
#                 '192.168.178.20',
#                 '192.168.178.30',
#                 '192.168.178.40',
#                 '192.168.178.50',
#                 '192.168.178.60',
#                 '192.168.178.70',
#                 '192.168.178.80']
#     casspiUser = 'pi'
#     casppiPassword = '1957'
# 
#     def __init__(self, ipList=casspiIP, user=casspiUser, password=casppiPassword):
#         self.ipList = ipList
#         self.user = user
#         self.password = password
#         self.client = paramiko.SSHClient()
#         self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 
#     def clusterShutdown(self):
#         command = 'sudo shutdown -h now'
# 
#         for ip in range(len(self.ipList)):
#             try:
#                 self.client.connect(self.ipList[ip], username=self.user, password=self.password)
#                 stdin, stdout, stderr = self.client.exec_command(command)
#                 print('Client {} fährt herunter...'.format(self.ipList[ip]))
#             except TimeoutError:
#                 print('Timeout! {} Bitte vergewissern Sie sich, dass der Client herunter fährt!'.format(self.ipList[ip]))
#             finally:
#                 self.client.close()
# 
#     def clusterReboot(self):
#         command = 'sudo reboot'
#         for ip in range(len(self.ipList)):
#             try:
#                 self.client.connect(self.ipList[ip], username=self.user, password=self.password)
#                 stdin, stdout, stderr = self.client.exec_command(command)
#                 print('Client {} startet neu...'.format(self.ipList[ip]))
#             except TimeoutError:
#                 print('Timeout! {} Bitte vergewissern Sie sich, dass der Client neustartet!'.format(self.ipList[ip]))
#             finally:
#                 self.client.close()
# =============================================================================


class Sqlite:
    def __init__(self):
        pass

    @staticmethod
    def connect(dbPathName):
        engineStringSQLite = r'sqlite:///' + dbPathName
        engine = sa.create_engine(engineStringSQLite)
        conn = engine.connect()
        return engine, conn

    @staticmethod
    def exo2sqlite(dbName, dataFile=None, dataFrame=None):
        if dataFile is not None:
            frame = pd.read_csv(dataFile, sep=';', header=0)
        elif dataFrame is not None:
            frame = dataFrame
        else:
            frame = None

        if frame is not None:
            # get tableName
            year = frame['dateTime'][0].strftime('%Y')
            tblName = 'tblExo' + year
            # connect
            dbPathName = os.path.join(dbName)
            conn = sqlite3.connect(dbPathName)
            # c = conn.cursor()
            # frame distinct Jahr ermitteln
            # schauen, ob Tabelle aktuelles(entsprechend der Daten) Jahr vorhanden
            # Falls nicht vorhanden --> anlegen
            # neuestes Datum abfragen (nicht bei neu angelegt)
            # frame entsprechend aufteilen
            # nur Daten hochladen, die noch nicht drin sind

            col = 'dateTime'

            # queryCreate = 'create table if not exists {}'.format(tblName)
            # queryAll = 'select * from {}'.format(tblName)
            queryMaxDate = 'select max({}) from {}'.format(col, tblName)
            queryCountRows = 'select count({}) from {}'.format(col, tblName)

            try:
                maxDateFrame = pd.read_sql_query(queryMaxDate, conn)
                rowsFrame = pd.read_sql_query(queryCountRows, conn)
                rows = rowsFrame.values[0][0]
                print('Anzahl Datensätze: {}'.format(rows))
                maxDate = maxDateFrame.values[0][0]
                maxDate = pd.Timestamp.strptime(maxDate, '%Y-%m-%d %H:%M:%f')
                print('Aktuell letzter Datensatz vom: {}'.format(maxDate))
                # print(maxDate[0][0])
            except Exception:
                print('create new table {}'.format(tblName))
                maxDate = None

            if maxDate is not None:
                choppedFrame = frame[frame['dateTime'] > maxDate]
                frame = choppedFrame

            if frame.empty is False:
                print('Daten werden hochgeladen...')
                frame.to_sql(tblName, conn, if_exists='append', index=False)
                newMaxDateFrame = pd.read_sql_query(queryMaxDate, conn)
                rowsFrame = pd.read_sql_query(queryCountRows, conn)
                rows = rowsFrame.values[0][0]
                print('Anzahl Datensätze: {}'.format(rows))
                newMaxDate = newMaxDateFrame.values[0][0]
                # newMaxDate = pd.to_datetime(newMaxDate, '%Y-%m-%d %H:%M:%f')
                print('Neuester Datensatz vom: {}'.format(newMaxDate))
            else:
                print('Datenbank ist aktuell. Keine neuen Daten vorhanden.')
        conn.close()
