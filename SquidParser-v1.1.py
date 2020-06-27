# SquidParser.py - A script to make reading Squid logs easier.
# License: Creative Commons - See Source for more details.
# Usage: python3 SquidParser.py
# Authors: Riskjuggler and son aka Steve and Louis
# Source: https://github.com/Riskjuggler/SquidParser
# Version 1.1

import sys, getopt
import time
from datetime import datetime, timedelta
import pymongo
from pymongo import MongoClient
import configparser
import os
from os.path import expanduser
import statistics
from array import *

class configFileOps(reuseconfig):
     def __init__(self):
        homeDir = expanduser("~")
        configFile = homeDir + "/.SquidParser/squidparser.conf"
        fileExists(configFile)
        continueRunOp(continuerun)

     def fileExists(configFile):
        if os.path.exists(configFile):    
            print("It appears you've run SquidParser before.")
            continuerun = input("Have you changed any of the database information? (y or n) : ")  # Need to be sure we can rely on previous info
            return continuerun

    def continueRunOp(continuerun):
        if continuerun == 'y':
            print ("Edit " + homeDir + "/SquidParser.conf to make changes using your favorite text editor.  Then re-start SquidParser.py")
            exit()
        else:
            return 

class reportInfoOps:
    def __init__(self):


class parseFlagOps:
    def __init__(self, opts, args):
        confignogood = True  # Only need to collect config if it's no good
        dbload = False   # Only need to load DB if it's not already loaded
        reportonly = False  # Normal is to load DB and report
        ipaddress = ""
        date = datetime(today) # TO DO: Need to get today in MMDDYYYY format
        for opt, arg in opts:   # Finish aligning with https://www.tutorialspoint.com/python/python_command_line_arguments.htm
            if arg == '-h':
                print 'SquidParser.py -c (-d or -r) -t <MMDDYYYY> -i <IP address>'
                sys.exit()
            elif arg == "-c":
                confignogood = False
            elif arg = "-d":
                dbloaded = True
            elif arg = "-r":
                reportonly = True
            elif arg = "-t":  # Need to fix this to get parameters too
                date = 
            elif arg = "-i":  # Need to fix this to get parameters too
                ipaddress = 
        return confignogood, dbload, reportonly

class dbOperations:
    def __init__(self):


class timeToolOps:
    def __init__(self):

# Main Method
def main(argv):
    opts, args = getopt.getopt(argv,"hcdrt:i:",["date=","ipaddress="])
    if getopt.GetoptError:
        print 'No flags or parameters so executing the fully manual approach.'
    else:
        parseflags=parseFlagOps(opts, args)  #first parse the flags

    if confignogood:  
        configenable=configFileOps(reuseconfig) # Next have to read config file

   dboper=DBOperations()
    # Get file name from user and parse and then read log and put in DB - DONE
    read = input("Have you loaded DB yet? (y/n) : ")
    if read == "n":
        ReadLog(GetLogFile(),dboper) # Done and working
        # Identify time delta between logs by source IP
        dboper.UpdateTimeDiff()

    # Do some statistics to help user decide what time diff to use in reporting
    print("As you should know, websites have a main URL which often calls many other URLs behind the scenese.  It is up to you to tell")
    print("me how to identify the difference between a main URL and it's related URLs.  This app is built on assumption that you")
    print("will pause between one web page and another longer than the computer will typically pause when calling related URls.")
    print("")
    print("Let's analyze the database to help you guess the # of seconds between calls to identify each distinct source:")
    dboper.analyzeRange()

    # Report if less than user provided value
    value=float(input("Provide # of seconds to report : "))
    ip_addr=input("Provide IP address to report : ")
    dboper.reportLessthantime(value, ip_addr)

# Main execution

if __name__ == '__main__':
    main()