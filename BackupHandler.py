from pysnmp.hlapi import *
# 3rd Lib
import random
import time
# Program Include
import Configload
import logging


class BackupHandler:
    def __init__(self):
        starttime = time.strftime("%Y%m%d%H%M", time.localtime())
        # if os.path.exists(starttime + '/log/Backup.log') is not True:
        #     with open(starttime + '/log/Backup.log', 'w') as f:
        #         f.close()
        logging.basicConfig(filename='log/' + starttime + '.log', filemode='w', level=logging.DEBUG,
                            format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
        self.__config = Configload.Config()
        self.__folder = starttime
        self.__cccopymib = 'CISCO-CONFIG-COPY-MIB'

    def __handlesinglebackup(self, node):
        entryindex = random.randint(1, 1000)
        logging.info('Select a session ID ' + str(entryindex))
        # Create an entry with random index and wait
        logging.info(next(setCmd(SnmpEngine(),
                                 CommunityData(self.__config.community),
                                 UdpTransportTarget((node['Ipaddress'], 161)),
                                 ContextData(),
                                 ObjectType(ObjectIdentity(self.__cccopymib, 'ccCopyEntryRowStatus', entryindex).
                                            addMibSource(self.__config.mibsrc), Integer(5)))  # Create Entry and wait
                          ))
        #
        # set backup configuration of single node via SNMP ccCopyEntry
        logging.info(next(setCmd(SnmpEngine(),
                                 CommunityData(self.__config.community),
                                 UdpTransportTarget((node['Ipaddress'], 161)),
                                 ContextData(),
                                 # Set copy protocol as tftp
                                 ObjectType(ObjectIdentity(self.__cccopymib, 'ccCopyProtocol', entryindex).
                                            addMibSource(self.__config.mibsrc), Integer(1)),
                                 # Set copy source as running-config
                                 ObjectType(ObjectIdentity(self.__cccopymib, 'ccCopySourceFileType', entryindex).
                                            addMibSource(self.__config.mibsrc), Integer(4)),
                                 # Set copy destination as network file
                                 ObjectType(ObjectIdentity(self.__cccopymib, 'ccCopyDestFileType', entryindex).
                                            addMibSource(self.__config.mibsrc), Integer(1)),
                                 # Set copy destination IP add
                                 ObjectType(ObjectIdentity(self.__cccopymib, 'ccCopyServerAddress', entryindex).
                                            addMibSource(self.__config.mibsrc), IpAddress(self.__config.tftpaddr)),
                                 # Set copy destination file name
                                 ObjectType(ObjectIdentity(self.__cccopymib, 'ccCopyFileName', entryindex).
                                            addMibSource(self.__config.mibsrc),
                                            self.__folder + '/' + node['Specification'] + '/' + node[
                                                'Nodename'] + '.conf'))

                          ))
        # trigger the backup process
        logging.info(next(setCmd(SnmpEngine(),
                                 CommunityData(self.__config.community),
                                 UdpTransportTarget((node['Ipaddress'], 161)),
                                 ContextData(),
                                 ObjectType(ObjectIdentity(self.__cccopymib, 'ccCopyEntryRowStatus', entryindex).
                                            addMibSource(self.__config.mibsrc), Integer(1)))
                          ))
        # destroy the entry
        logging.info(next(setCmd(SnmpEngine(),
                                 CommunityData(self.__config.community),
                                 UdpTransportTarget((node['Ipaddress'], 161)),
                                 ContextData(),
                                 ObjectType(ObjectIdentity(self.__cccopymib, 'ccCopyEntryRowStatus', entryindex).
                                            addMibSource(self.__config.mibsrc), Integer(6)))
                          ))
        return True

    def startfullbackup(self):
        for node in self.__config.nodelist:
            self.__handlesinglebackup(node)
