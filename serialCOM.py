# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 23:43:37 2020

@author: thch1015
"""

import serial
import serial.tools.list_ports
import toolsCT as tools
import platform


def prepare_connection(master=False):
    infomessage_1 = 'Bitte schließen Sie die Controllerplatine\n' \
                  'mittels USB-Kabel an den PC an!\n' \
                  'Drücken Sie anschließend "Ok"!'
    infomessage_2 = 'Bitte resetten Sie den Controller\n' \
                    'und starten Sie das Programm neu!\n' \
                    'Falls das Problem weiterhin besteht,\n' \
                    'ist möglicherweise der PSoC defekt.'
    TIMEOUT = False
    timeoutCounter = 0
    while True:
        ports = serial.tools.list_ports.comports()
        machine = platform.system()
        print(machine)
        if machine == 'Linux':
            for p in ports:
                print(p.description)
                if 'USBUART' in p.description:
                    port = p.device
                    # print(port)
                    break
                else:
                    port = False
            if port is False:
                if timeoutCounter < 5:
                    timeoutCounter += 1
                    TIMEOUT = False
                    tools.infobox(infomessage_1)
                else:
                    TIMEOUT = True

        if machine == 'Windows':
            for p in ports:
                print(p.description)
                if 'Serielles' in p.description:
                    port = p.device
                    # print(port)
                    break
                else:
                    port = False
            if port is False:
                if timeoutCounter <= 5:
                    timeoutCounter += 1
                    TIMEOUT = False
                    tools.infobox(infomessage_1)
                else:
                    TIMEOUT = True
        if port is not False:
            break
        if TIMEOUT is True:
            tools.errorbox(infomessage_2)
            raise ConnectionError
    if master is True:
        try:
            session = InterfacePsocMaster(port)
        except ConnectionError:
            tools.errorbox('Bitte Kabelverbindung prüfen, Controller resetten und\n'
                           'Programm neu starten!')
            raise ConnectionError
    else:
        try:
            session = InterfacePsocSlave(port)
        except ConnectionError:
            tools.errorbox('Bitte Kabelverbindung prüfen, Controller resetten und\n'
                           'Programm neu starten!')
            raise ConnectionError
    return session


class InterfacePsocSlave:
    """
    """
    def __init__(self, port=None, baudrate=115200):
        self.session = serial.Serial(port, baudrate)

    def open_port(self):
        if self.session.is_open is False:
            try:
                self.session.open()
            except:
                print('Ist der Port ausgewählt?')
        else:
            pass

    def close_port(self):
        self.session.close()

    def transmit(self, order=b'm'):
        try:
            self.session.write(order)  # Ausnahme prüfen wg Absturz!
        except:
            print("Kabelverbindung prüfen!")

    def receive(self):
        received = self.session.readline()
        received = received.decode()
        return received

    def getUart(self):
        self.open_port()
        self.transmit()
        dataString = self.receive()
        self.close_port()  # führt möglicherweise zur Blockade im PSoC
        return dataString


class InterfacePsocMaster:
    """
    Noch nicht fertig...
    """
    def __init__(self, port=None, baudrate=115200):
        self.session = serial.Serial(port, baudrate)

    def open_port(self):
        if self.session.is_open is False:
            try:
                self.session.open()
            except:
                print('Ist der Port ausgewählt?')
        else:
            pass

    def close_port(self):
        self.session.close()

    def transmit(self, order=b'm'):
        try:
            self.session.write(order)  # Ausnahme prüfen wg Absturz!
        except:
            print("Kabelverbindung prüfen!")

    def receive(self):
        received = self.session.readline()
        received = received.decode()
        return received

    def getUart(self):
        self.open_port()
        self.transmit()
        dataString = self.receive()
        self.close_port()  # führt möglicherweise zur Blockade im PSoC
        return dataString

