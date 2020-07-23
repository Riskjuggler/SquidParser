# SquidParser.py - A script to make reading Squid logs easier.
# License: Creative Commons - See Source for more details.
# Usage: python3 SquidParser.py
# Authors: Riskjuggler and son aka Steve and Louis
# Source: https://github.com/Riskjuggler/SquidParser
# Version 1.1

import sys, getopt
import time
from datetime import datetime, timedelta, date
import pymongo
from pymongo import MongoClient
import configparser
import os
from os.path import expanduser
import statistics
from array import *

class configFileOps(configgood):
     def __init__(self):
        # Establish default parameters containing config file pointer
        homeDir = expanduser("~")
        configFile = homeDir + "/.SquidParser/squidparser.conf"
        configPath = homeDir + "/.SquidParser"
        # Need to check if the file already exists
        if os.path.exists(configFile):    
            if configgood == True:
                continuerun = "y"
            else:
                continuerun = input("Have you changed any of the database information? (y or n) : ")  # Need to be sure we can rely on previous info
            # Based on input from user, define connectionstring or exit because the config file needs modification
            if continuerun == "y":
                connectionString = configFileOps.readConfig(configFile)
            else:
                # For now we don't have code to enable changes so have user manually edit and restart.
                print("Exiting so you can edit the config file manually and restart SquidParser.py")
                exit()
        else:
            # If config file doesn't exist, need to create it
            connectionString = configFileOps.addConfig(configPath, configFile)
        return connectionString

    def addConfig(configPath, configFile):
        print("This is the first time running SquidParser on this system so we need some information before we can begin.")
        mongodbserver = input("What is the IP address of the MongoDB server? ")
        mongodbuser = input("What is the userID to use to access MongoDB? ")
        mongodbpass = input("What is the password of the MongoDB? ")
        mongodblocation = input("What is the location of the MongoDB? ")
        mongodbclustername = input("What is the cluster name for the MongoDB? ")
        mongodbcollection = input("What is the collection name in the MongoDB? ")
        print("Writing to config file...")
        print("NOTE: Passwords are NOT encrypted when stored!!! Make sure that ~/SquidParser/config.txt is protected!!")
        config_object = configparser.RawConfigParser()
        config_object["mongodb"] = {
            "mongodbserver" : mongodbserver ,
            "mongodbuser" : mongodbuser ,
            "mongodbpass" : mongodbpass ,
            "mongodblocation" : mongodblocation ,
            "mongodbclustername" : mongodbclustername ,
            "mongodbcollection" : mongodbcollection }
            if os.path.exists(configPath):   # If config does not exist, make directory first
                print("Config directory already exists.  A little odd but will continue.")
            else:
                os.mkdir(homeDir + '/.SquidParser')
            # Create the file and add the content for next time
            with open(configFile, 'w') as conf:    
                config_object.write(conf)
        connectionString = "mongodb://" + mongodbuser + ":" + mongodbpass + "@" + mongodbserver + ":27017/" + mongodblocation + "?retryWrites=true&w=majority"
        return connectionString

    # def readConfig(configFile):
        configparserfunc = configparser.RawConfigParser()  # Need to parse the config file to get local info
        configparserfunc.read(configFile)
        mongodbserver = configparserfunc.get('mongodb', 'mongodbserver')  # Need to know the IP or hostname of the DB server
        mongodbuser = configparserfunc.get('mongodb', 'mongodbuser') # Need to know the userID to access the DB server
        mongodbpass = configparserfunc.get('mongodb', 'mongodbpass')  # Need to know the password
        mongodblocation = configparserfunc.get('mongodb', 'mongodblocation') # Need to know the folder where the DB is 
        mongodbclustername = configparserfunc.get('mongodb', 'mongodbclustername')  # Need to know the cluster name
        mongodbcollection = configparserfunc.get('mongodb', 'mongodbcollection') # Need to know the name of the collection 
        connectionString = "mongodb://" + mongodbuser + ":" + mongodbpass + "@" + mongodbserver + ":27017/" + mongodblocation + "?retryWrites=true&w=majority"
        return connectionString

    # def columnstoUse():
    #     sdf


# class reportOps:
#     def __init__(self):
#         dfsd

    # def byIP():
    #     sdf

    # def byDate():
    #     sdf

    # def byParentURL():
    #     sdf

class parseFlagOps():
    def __init__(self):
        # Placeholder just in case for future

    def iterateFlags(optlist, args):
        configgood = True  # Only need to collect config if it's no good
        loadflag = False   # Only need to load DB if it's not already loaded
        reportall = False  # Normal is to load DB and report
        ipaddress = ""
        datetoreport = date.today().strftime('%m/%d/%Y')  
        timeDiff = 0
        logFile = ""
        for opt, arg in optlist:   # Finish aligning with https://www.tutorialspoint.com/python/python_command_line_arguments.htm
            if opt == "-h":
                print("There are 5 unique ways to execute SquidParser.py")
                print("The most manual way is by simply executing python SquidParser.py which will ask you multiple questions along the way to provide the report")
                print("for a single IP across all days in the logs ever loaded.")
                print()
                print("To speed things up you can indicate if a previously defined config file already exists by adding -c.  The config file is expected to be at ~/.SquidParser/config.txt")
                print("See README-configfile.md for more details on manually creating the config file.")
                print()
                print("-l will indicate you only want to load the data from an identified log file.  Example: python SquidParser.py -l <filename with path>")
                print("Note: At this time SquidParser can only process a single log file per execution.")
                print("Note:  To fully automate periodic processing of logs, include the -c flag when using -l")
                print("-r will indicate you only want to report from existing data.  You will be asked to provide the IP and timeDiff value Example: python SquidParser.py -c -r")
                print("With -r you can also include -i <IP address>, -d <MMDDYYY>, and -t <timeDiff>  to skip all further data entry.  This is the most useful for automated reporting.")
                print("If you are unsure what timeDiff to use, you can use -m to perform some deeper analysis of the timeDiff values.")  
                print("If you don't provide the -i <IP address>, -d <MMDDYYY> with -m you will get a report for all IPs across all the data.")
                print()
                print("Of course you can put all these together: python SquidParser.py -c -l <filename with path> -r -i <IP Address> -d <MMDDYYY> -t <timeDiff>")
                print("This will completely automate a single days load and report to STDOUT.")
                sys.exit(2)
            elif optlist == "-c":
                configgood = False
            elif optlist == "l":  
                logFile = arg
            elif opt == "-r":
                reportall = True
            elif opt == "-d":  
                datetoreport = arg 
            elif opt == "-t":  
                timeDiff = arg
            elif opt == "-i":  
                ipaddress = arg
        print("Outputs : ",configgood, reportall, datetoreport, timeDiff, ipaddress, logFile)  # Just here for QA - comment for Prod
        return configgood, reportall, datetoreport, timeDiff, ipaddress, logFile

    
class mongoDBoperations(configgood):
    def __init__(self):
        #        

    def mongofromConfig(configgood):
        # First get the connection string from the config file
        connectionString=configFileOps(configgood)
        # Establish the connection
        collection = self.establishConnection(connectionstring)
        return collection  

    def establishConnection(connectionstring):
        self.cluster = MongoClient(connectionString)
        self.db = self.cluster[mongodbclustername]
        self.collection = self.db[mongodbcollection]
        return collection

    # def readData(collection, query):
    #     sdf

    # def readCols():
    #     sdf

    # def columnExport():
    #     sdf

    # def loadData():
    #     sdf

        # Insert one post into MongoDB
    def MongoInsertOne(self, post):
        self.collection.insert_one(post)

    # Define method to iterate over lines using dict to identify parse column and string to identify time diff to update 
    def UpdateTimeDiff(UpdateTimeDiff):
        # Find all the source IPs first - NEEDS WORK - See design bug about dual loops
        distinctList = self.collection.distinct("clientAddress")
        for clientAddress in distinctList:
            timeStampPrevious = 0.0
            allpostsforIP = self.collection.find({"clientAddress":clientAddress})
            for timestamp in allpostsforIP:
                timeStampCurrent = timestamp["logTime"]
                timeDiff_var = measureTimeDiff(timeStampCurrent, timeStampPrevious)
                record_data = {"timeDiff":timeDiff_var}
                self.collection.update_one({"logTime" : timeStampCurrent}, {"$set":record_data})  
                timeStampPrevious = timeStampCurrent

    # Define method to report entries who's timeDiff < passed value
    def reportLessthantime(self, value, clientAddressInstance):
        if clientAddressInstance != "-":    
            print("Reporting for", clientAddressInstance, "log entries that occured greater than ", value, "seconds since the previous entry.")
            for onetimeDiff in self.collection.find({"clientAddress":clientAddressInstance}):
                timeDiff_var = onetimeDiff["timeDiff"]
                if timeDiff_var >= value:
                    logTime = datetime.utcfromtimestamp(float(onetimeDiff["logTime"]))-timedelta(hours=6)
                    duration = onetimeDiff["duration"]
                    clientAddress = onetimeDiff["clientAddress"]
                    resultCode = onetimeDiff["resultCode"]
                    siteBytes = onetimeDiff["siteBytes"]
                    siteUrl = onetimeDiff["siteUrl"]
                    userId = onetimeDiff["userId"]
                    hierarchyCode = onetimeDiff["hierarchyCode"]
                    callType = onetimeDiff["callType"]
                    print(logTime, ";", clientAddress, ";", resultCode, ";", siteUrl, ";", callType, ";", timeDiff_var)

    # Need to provide some statistical analysis of the timeDiff values to help the user decide which to use across all IPs in the DB
    def analyzeRangeallIPs():
        # Get all IPs in the DB
        distinctList = self.collection.distinct("clientAddress")
        for clientAddressInstance in distinctList:
            # Need to avoid working with null values
            if clientAddressInstance != "-":    
                print("Reporting stats for", clientAddressInstance)
                self.analyzeRangeoneIP(clientAddressInsance)


    # Need to provide some statistical analysis of the timeDiff values to help the user decide which to use across one IP in the DB
    def analyzeRangeoneIP(clientAddressInstance):
        # Start an array to store timeDiff values
        timeDiff_arr = array("f",[])
        # Need to avoid working with null values
        print("Reporting stats for", clientAddressInstance)
        # Get all posts for the IP
        allpostsforIP = self.collection.find({"clientAddress":clientAddressInstance})
        # Create an array with all the timeDiff values matching the IP
        for element in allpostsforIP:
            timeDiff_arr.append(float(element["timeDiff"]))
        # Need to sort so we can get rid of the inevitable large first value
        timeDiff_arrsorted = sorted(timeDiff_arr)
        timeDiff_arrsorted.pop()
        # Get some stats info for the IP
        dataAnalyze.basicStats(timeDiff_arrsorted)         

class squidProcessing():
    # Define method to collect the name and location of a single file to be processed - DONE
    def getsquidlogfileManual():
            filename = input("Please provide filename with path.  If you do not provide path, we will assume the file is in the current working directory. : ")
            return filename

    # Parse each line into separate variable  - DONE
    def ParseSquidLine(arrayLine):
        post = {
        "logTime" : arrayLine[0],
        "duration" : arrayLine[1],
        "clientAddress" : arrayLine[2],
        "resultCode" : arrayLine[3],
        "siteBytes" : arrayLine[4],
        "callType" : arrayLine[5],
        "siteUrl" : arrayLine[6],
        "userId" : arrayLine[7],
        "hierarchyCode" : arrayLine[8],
        "timeDiff" : 0,
        }
        return post





class timeToolOps:
    def __init__(self):
        sdgf

    # Measure gap to next call - DONE
    def measureTimeDiff(timestampCurrent, timestampPrevious):
        diff = datetime.utcfromtimestamp(float(timestampCurrent)/1000) - datetime.utcfromtimestamp(float(timestampPrevious)/1000)
        timeDiff = diff.total_seconds()
        return timeDiff

    def timeStats():
        sdf

# Need a class to perform stats and any machnine learning
class dataAnalyze():
    def __init__(self):
        sdf

    # To be ready to do Machine Learning, need to have headers of the data
    def convertHeadersfromMongo():
        sdf

    # Need to get more meaningful stats info about an array
    def shape_Data():
        sdf

    # Need to be able to provide basic statistics for an array
    def basicStats(array):
        print("Mean : " , statistics.mean(array))
        print("Median : " , statistics.median(array))
        print("Min : " , min(array))
        print("Max : " , max(array))
        print("----------------------------------------------")
        print("Multimode :" + statistics.multimode(timeDiff_arr)) 

# Squid was the first of the log types we needed to process
class squidProcessing:
    def __init__(self):
        sdf

    # The way to guess a parent from a child is to measure the difference in time stamps between subsequent lines
    def MeasureTimeDiff():
        sdf

    # Need to parse the squid data into variables
    def ParseSquidLine():
        sdf

    # Define method to iterate over lines in the file feed content to ProcessLine- DONE
    def ReadLog(filename, mongocollection):
        # Need to set initial previous timestamp as present time - Note: This will result in large timeDiff value
        timestampPrevious=time.time()
        # Now open the logfile for reading
        with open(filename, "r") as fp: # SECURITY RISK: Need to worry about injection attacks later
            # Read each line of the file
            for line in iter(fp.readline, ''):
                # parse the row into an element in an array
                arrayLine = [array for array in str.split(line)]
                # Define a Mongo document for posting
                # Note: Need to update this after we add other DB types
                post = ParseSquidLine(arrayLine)
                # Add the document to the mongo DB
                mongocollection.MongoInsertOne(post)

    
# Main Method
def main():

    # Set initial parameters
    configgood = False  # Only need to collect config if it's no good.  Assume config doesn't exist as default.
    loadflag = True   # Only need to load DB if it's not already loaded   Assume data is not loaded.
    reportall = True  # Normal is to load DB and then report from all days but allow user to enter IP   
    ipaddress = ""   # Default is to ask the user for IP to filter report
    datetoreport = date.today().strftime('%m/%d/%Y')  # Need to establish datavar as date format
    timethreshold = float(0)    # Need to establish timeDiff as float type
    logfile = "./access.log"   # Default is that the job is run while the user is in the same directory as the access.log file

    # Get any options that were provided
    optlist, args = getopt.getopt(sys.argv[1:], 'hcri:d:t:')  
    print("Optlist : ", optlist)  # These are for QA, comment out before moving to Production
    print("Args : ", args)   # These are for QA, comment out before moving to Production

    # Need to handle when no options provided - This was the default v1.0 function and leads to performing all major functions
    if optlist == []:
        print('No flags or parameters so executing the fully manual approach.')  
    else:
        # Get the values from the command line
        configgood, reportall, datetoreport, timethreshold, ipaddress, logFile=parseFlagOps.iterateFlags(optlist, args)  #first parse the flags
    # This is for QA purposes.  Comment out in Prod
    print("Values for processing : ",configgood, reportall, datetoreport, timeDiff, ipaddress)  

    # Enable DB for any further activities
    # Note - need to add decision here later when we support more storage options
    # Need to get the MongoDB collection to use

    mongocollection=mongoDBoperations.mongofromConfig(self, configgood)

    # Need to load logs only if user wants us to - default is to load logs
    if loadflag:
        # Default is to assume that config may not exist or be trustworthy
        if configgood == False:
            # Get file name from user and parse and then read log and put in DB - DONE
            # When we add more log types need to expand this
            filename=squidProcessing.getsquidlogfileManual()
        else:
            # Filename is either the default or the value from the command line
            filename=logfile 
        # Now we can read the log and write it into the DB    
        squidProcessing.ReadLog(filename,mongocollection) 

        # Identify time delta between logs by source IP
        mongoDBoperations.UpdateTimeDiff(mongocollection)

        # Need to report if user wants to - default is to report from entire DB

        # Provide some simple statistical analysis to help user decide what timeDiff to use when reporting
        print("As you should know, websites have a main URL which often calls many other URLs behind the scenese.  It is up to you to tell")
        print("me how to identify the difference between a main URL and it's related URLs.  This app is built on assumption that you")
        print("will pause between one web page and another longer than the computer will typically pause when calling related URls.")
        print("")
        print("Let's analyze the database to help you guess the # of seconds between calls to identify each distinct source:")
        mongoDBoperations.analyzeRangeallIPs()

        # Report if less than user provided value
        value=float(input("Provide # of seconds to report : "))
        ip_addr=input("Provide IP address to report : ")
        mongoDBoperations.reportLessthantime(value, ip_addr)
        exit()


    # v 1.1 functionality - Execute based on command line flags 

    if reportall = False:
        squidProcessing.ReadLog(squidProcessing.getsquidlogfileManual(),mongocollection) 

    # Perform analysis and report if flag says to report
    # 





# Main execution

if __name__ == '__main__':
    main()