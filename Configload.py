import configparser
import csv
import sys
import os
import logging
import argparse


class Config:
    def __init__(self, location=sys.path[0] + '/Conf/backup.conf'):
        self.__cliargs = None
        self.__readconfigfromcli()
        if self.__cliargs.debug:
            logging.basicConfig(level=logging.DEBUG)
        if self.__cliargs.gconfig is True:
            logging.info('Redirect the configuration file to' + self.__cliargs.gconfig)
            location = self.__cliargs.gconfig
        if os.path.exists(location) is True:
            logging.info('Find Backup.conf in ' + location)
        else:
            logging.critical('Could not find the configuration file in ' + location)
            exit()
        # override the global config if specified in cli
        config = configparser.ConfigParser()
        config.read(location)
        self.__nodeconf = sys.path[0] + config['SNMP']['NodeConf']
        self.__port = int(config['SNMP']['SNMPPort'])
        self.__community = config['SNMP']['Community']
        self.__mibsrc = sys.path[0] + config['SNMP']['MIBSrc']
        self.__snmpmode = config['SNMP']['SNMPMode']
        self.__protocol = config['BACKUP']['Protocol']
        self.__tftpaddr = config['BACKUP']['TFTPAddr']
        self.__nodelist = []
        self.loadcsv(sys.path[0] + config['SNMP']['NodeConf'])

    @property
    def nodeconf(self):
        return self.__nodeconf

    @property
    def port(self):
        return self.__port

    @property
    def community(self):
        return self.__community

    @property
    def mibsrc(self):
        return self.__mibsrc

    @property
    def snmpmode(self):
        return self.__snmpmode

    @property
    def protocol(self):
        return self.__protocol

    @property
    def tftpaddr(self):
        return self.__tftpaddr

    @property
    def nodelist(self):
        return self.__nodelist

    def loadcsv(self, nodecsv=sys.path[0] + '/Conf/node.csv'):
        if self.__cliargs.nodecsv is True:
            nodecsv = self.__cliargs.nodecsv
        if os.path.exists(nodecsv) is not True:
            logging.critical('Could not find the node csv file in ' + nodecsv)
        nodecsv = nodecsv
        with open(nodecsv, newline='') as ipcsv:
            nodereader = csv.DictReader(ipcsv, delimiter=',')
            for noderow in nodereader:
                self.__nodelist.append(noderow)

    def __readconfigfromcli(self):
        argparser = argparse.ArgumentParser()
        argparser.add_argument("--gconfig", help="Specify global configuration file with absolute path")
        argparser.add_argument("--nodecsv", help="Specify node csv configuration file with absolute path")
        argparser.add_argument("-d", "--debug", help="Logging detail information of the program",
                               action="store_true")
        self.__cliargs = argparser.parse_args()
