# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 10:35:22 2018

@author: thch1015
"""


class Casspi:
    # erstellt einen Keyspace
    queryCreateKeyspaceNTS33 = """CREATE KEYSPACE IF NOT EXISTS %s
                WITH replication = {'class':'NetworkTopologyStrategy',
                'DC1':'3', 'DC2':'3'}
    """

    # erstellt eine Tabelle für Exotenhausdaten
    queryCreateTableExo = """CREATE TABLE IF NOT EXISTS {}.{} (
                datetime timestamp,
                day text,
                month text,
                id text,
                batvolt float,
                rssi float,
                seq float,
                uptime float,
                objtemp float,
                airpres float,
                hdchumi float,
                abshumi float,
                hdctemp float,
                ambtemp float,
                amblight float,
                PRIMARY KEY ((datetime, id), month, day, batvolt,
                rssi, seq, uptime, objtemp, airpres, hdchumi, abshumi,
                hdctemp, ambtemp, amblight)
                ) with clustering order by (month desc, day desc)
    """

    # erstellt einen zusätzlichen Index für eine Filterspalte
    queryCreateIdx = """create index if not exists on {}.{} ({})
    """

    # erstellt einen INSERT-Befehl für Exotenhausdaten
    queryInsertExoAll = """INSERT INTO {}.{} (
                datetime,
                day,
                month,
                id,
                batvolt,
                rssi,
                seq,
                uptime,
                objtemp,
                airpres,
                hdchumi,
                abshumi,
                hdctemp,
                ambtemp,
                amblight)
                VALUES (%(datetime)s,
                        %(day)s,
                        %(month)s,
                        %(id)s,
                        %(batvolt)s,
                        %(rssi)s,
                        %(seq)s,
                        %(uptime)s,
                        %(objtemp)s,
                        %(airpres)s,
                        %(hdchumi)s,
                        %()abshumis,
                        %(hdctemp)s,
                        %(ambtemp)s,
                        %(amblight)s)
    """

    # Abfrage des Maximalwertes einer beliebigen Spalte
    queryMax = """select max({}) from {}.{}
    """

    # Abfrage der Anzahl Werte einer beliebigen Spalte
    queryCount = """select count({}) from {}.{}
    """


class Sqlite:
    # Abfrage des Maximalwertes einer beliebigen Spalte
    queryMax = """select max({}) from {}
    """

    # Abfrage der Anzahl Werte einer beliebigen Spalte
    queryCount = """select count({}) from {}
    """

    # Abfrage aller Exotenhausdaten in einem bestimmten Intervall
    queryAllInterval = """select *
    from {}   -- tablename
    where dateTime between '{}' and '{}' -- start and end
    """

    # Abfrage aller Exotenhausdaten in einem bestimmten Intervall
    # gefiltert nach Sensorname
    queryAllIntervalSensor = """select *
    from {}   -- tablename
    left join tblExoLevels on tblExoLevels.exo_id = {}.ID --tablename
    where dateTime between '{}' and '{}' -- start and end
    and name = {} -- sensor
    """

    # Abfrage bestimmter Spalten der Exotenhausdaten in einem bestimmten
    # Intervall, gefiltert nach Sensorname
    queryColsIntervalSensor = """select {} -- columns
    from {}   -- tablename
    left join tblExoLevels on tblExoLevels.exo_id = {}.ID --tablename
    where dateTime between '{}' and '{}' -- start and end
    and name = {} -- sensor
    """


