# SquidReporter.py - A script to make reading Squid logs easier.
# License: Creative Commons - See Source for more details.
# Usage: python3 SquidReporter.py
# Authors: Riskjuggler and son aka Steve and Louis
# Source: https://github.com/Riskjuggler/SquidReporter
# Version 1.0

import time
from datetime import datetime, timedelta
import pymongo
from pymongo import MongoClient
import configparser
import os
from os.path import expanduser
import statistics
from array import *

class DBOperations:

    def __init__(self):
        homeDir = expanduser("~")
        configFile = homeDir + "/.SquidReporter/squidreporter.conf"
        if os.path.exists(configFile):    
            print("It appears you've run SquidReporter before.")
            continuerun = input("Have you changed any of the database information? (y or n) : ")  # Need to be sure we can rely on previous info
            if continuerun == 'y':
                print ("Edit " + homeDir + "/SquidReporter.config.txt to make changes using your favorite text editor.  Then re-start SquidReporter.py")
                exit()
            configparserfunc = configparser.RawConfigParser()  # Need to parse the config file to get local info
            configparserfunc.read(configFile)
            mongodbserver = configparserfunc.get('mongodb', 'mongodbserver')  # Need to know the IP or hostname of the DB server
            mongodbuser = configparserfunc.get('mongodb', 'mongodbuser') # Need to know the userID to access the DB server
            mongodbpass = configparserfunc.get('mongodb', 'mongodbpass')  # Need to know the password
            mongodblocation = configparserfunc.get('mongodb', 'mongodblocation') # Need to know the folder where the DB is 
            mongodbclustername = configparserfunc.get('mongodb', 'mongodbclustername')  # Need to know the cluster name
            mongodbcollection = configparserfunc.get('mongodb', 'mongodbcollection') # Need to know the name of the collection 
        else:
            print("This is the first time running SquidReporter on this system so we need some information before we can begin.")
            mongodbserver = input("What is the IP address of the MongoDB server? ")
            mongodbuser = input("What is the userID to use to access MongoDB? ")
            mongodbpass = input("What is the password of the MongoDB? ")
            mongodblocation = input("What is the location of the MongoDB? ")
            mongodbclustername = input("What is the cluster name for the MongoDB? ")
            mongodbcollection = input("What is the collection name in the MongoDB? ")
            print("Writing to config file...")
            print("NOTE: Passwords are NOT encrypted when stored!!! Make sure that ~/SquidReporter/config.txt is protected!!")
            config_object = configparser.RawConfigParser()
            config_object["mongodb"] = {
                "mongodbserver" : mongodbserver ,
                "mongodbuser" : mongodbuser ,
                "mongodbpass" : mongodbpass ,
                "mongodblocation" : mongodblocation ,
                "mongodbclustername" : mongodbclustername ,
                "mongodbcollection" : mongodbcollection }

            homeDir = expanduser("~")
            configPath = homeDir + "/.SquidReporter"
            configFile = homeDir + '/.SquidReporter/config.txt'
            if os.path.exists(configPath):   # If config does not exist, make directory first
                print("Config directory already exists.  A little odd but will continue.")
            else:
                os.mkdir(homeDir + '/.SquidReporter')

            with open(configFile, 'w') as conf:    # Create the file and add the content for next time
                config_object.write(conf)
        connectionString = "mongodb://" + mongodbuser + ":" + mongodbpass + "@" + mongodbserver + ":27017/" + mongodblocation + "?retryWrites=true&w=majority"
        self.cluster = MongoClient(connectionString)
        self.db = self.cluster[mongodbclustername]
        self.collection = self.db[mongodbcollection]

    # Insert one post into MongoDB - DONE
    def MongoInsertOne(self, post):
        # Insert the post fed to the function
        self.collection.insert_one(post)

    # Define method to iterate over lines using dict to identify parse column and string to identify time diff to update - NEEDS WORK
    def UpdateTimeDiff(self):
        # Find all the source IPs first - NEEDS WORK - See design bug about dual loops
        distinctList = self.collection.distinct("clientAddress")
        for clientAddress in distinctList:
            timeStampPrevious = 0.0
            allpostsforIP = self.collection.find({"clientAddress":clientAddress})
            for timestamp in allpostsforIP:
                timeStampCurrent = timestamp["logTime"]
                timeDiff_var = measureTimeDiff(timeStampCurrent, timeStampPrevious)
                record_data = {"timeDiff":timeDiff_var}
                self.collection.update_one({"logTime" : timeStampCurrent}, {"$set":record_data})  # Test this once the post is right - NEEDS WORK
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

    def analyzeRange(self):
        distinctList = self.collection.distinct("clientAddress")
        for clientAddressInstance in distinctList:
            timeDiff_arr = array("f",[])
            if clientAddressInstance != "-":    
                print("Reporting stats for", clientAddressInstance)
                allpostsforIP = self.collection.find({"clientAddress":clientAddressInstance})
                for element in allpostsforIP:
                    timeDiff_arr.append(float(element["timeDiff"]))
                timeDiff_arrsorted = sorted(timeDiff_arr)
                timeDiff_arrsorted.pop()
                print("Mean : " , statistics.mean(timeDiff_arrsorted))
                print("Median : " , statistics.median(timeDiff_arrsorted))
                print("Min : " , min(timeDiff_arrsorted))
                print("Max : " , max(timeDiff_arrsorted))
                print("----------------------------------------------")
#                print("Multimode :" + statistics.multimode(timeDiff_arr))  # Needs to run on Python 3.8 for this to work
                
# Define method to collect the name and location of a single file to be processed - DONE
def GetLogFile():
        filename = input("Please provide filename with path.  If you do not provide path, we will assume the file is in the current working directory. : ")
        return filename

# Measure gap to next call - DONE
def measureTimeDiff(timestampCurrent, timestampPrevious):
    diff = datetime.utcfromtimestamp(float(timestampCurrent)/1000) - datetime.utcfromtimestamp(float(timestampPrevious)/1000)
    timeDiff = diff.total_seconds()
    return timeDiff

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

# Define method to iterate over lines in the file feed content to ProcessLine- DONE
def ReadLog(filename, dboper):
    timestampPrevious=time.time()
    with open(filename, "r") as fp: # SECURITY RISK: Need to worry about injection attacks later
        for line in iter(fp.readline, ''):
            arrayLine = [array for array in str.split(line)]
            post = ParseSquidLine(arrayLine)
            dboper.MongoInsertOne(post)

# Main code

dboper=DBOperations()

# Get file name from user and parse and then read log and put in DB - DONE
read = input("Have you loaded DB yet? (y/n) : ")
if read == "n":
    ReadLog(GetLogFile(),dboper) # Done and working
    # Identify time delta between logs by source IP
    dboper.UpdateTimeDiff()

# Do some statistics to help decide what time diff to use in reporting
print("Let's analyze the database to help guess the # of seconds to use per distinct source:")
dboper.analyzeRange()

# Report if less than user provided value
value=float(input("Provide # of seconds to report : "))
ip_addr=input("Provide IP address to report : ")
dboper.reportLessthantime(value, ip_addr)
