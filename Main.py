import BackupHandler
import sys,getopt
import optparse

if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "h", ["conf=", "tftp=", "mibsrc="])
    for option, value in opts:
        if option is '-h':
            sys.exit(0)
        if option is ''