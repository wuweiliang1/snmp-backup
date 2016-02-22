import BackupHandler
import argparse


class Entry:
    def __init__(self):
        configparser = argparse.ArgumentParser()
        configparser.add_argument("--gconfig", help="Specify global configuration file with absolute path")
        configparser.add_argument("--nodecsv", help="Specify node csv configuration file with absolute path")
        configparser.add_argument("-d", "--debug", help="Logging detail information of the program",
                                  action="store_true")
        configparser.add_argument("-s", "--single", help="Backup single node config(use together with --ip)",
                                  action="store_true")
        configparser.add_argument("--ip", help="Specify single backup node ip", type=str)
        self.args = configparser.parse_args()
entry = Entry()
backuphandler = BackupHandler.BackupHandler()
backuphandler.startfullbackup()
