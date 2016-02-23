import BackupHandler


class Main:
    def __init__(self):
        backuphandler = BackupHandler.BackupHandler()
        backuphandler.startfullbackup()

if __name__ == "__main__":
    main = Main()
