#imports
import time
from datetime import datetime, timedelta
import pymongo
from pymongo import MongoClient
import configparser
import os
from os.path import expanduser


# need to include DB Operations

class DBOperations:

    def mongofromConfig():    
        homeDir = expanduser("~")
        configFile = homeDir + "/.SquidParser/squidparser.conf"
        
        # TO DO: Need to add flag check to see if configFile is valid or from another file before building a new one

        if os.path.exists(configFile):    # Allow for previous existence but check to see if re-use is desired
            print("It appears you've run SquidParser before.")
            continuerun = input("Have you changed any of the database or other information? (y or n) : ")  # Need to be sure we can rely on previous info
            if continuerun == 'y':
                print ("Edit " + homeDir + "/SquidParser.conf to make changes using your favorite text editor.  Then re-start SquidParser.py")
                exit()  # If it already exists, the user should be able to edit manually - TO DO: Need to update documentation to explain config file fields.
            configparserfunc = configparser.RawConfigParser()  # Need to parse the config file to get local info
            configparserfunc.read(configFile)
            mongodbserver = configparserfunc.get('mongodb', 'mongodbserver')  # Need to know the IP or hostname of the DB server
            mongodbuser = configparserfunc.get('mongodb', 'mongodbuser') # Need to know the userID to access the DB server
            mongodbpass = configparserfunc.get('mongodb', 'mongodbpass')  # Need to know the password
            mongodblocation = configparserfunc.get('mongodb', 'mongodblocation') # Need to know the folder where the DB is 
            mongodbclustername = configparserfunc.get('mongodb', 'mongodbclustername')  # Need to know the cluster name
            mongodbcollection = configparserfunc.get('mongodb', 'mongodbcollection') # Need to know the name of the collection 
        else:
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

            homeDir = expanduser("~")
            configPath = homeDir + "/.SquidParser"
            configFile = homeDir + '/.SquidParser/squidparser.conf'
            if os.path.exists(configPath):   # If config does not exist, make directory first
                print("Config directory already exists.  A little odd but will continue.")
            else:
                os.mkdir(homeDir + '/.SquidParser')

            with open(configFile, 'w') as conf:    # Create the file and add the content for next time
                config_object.write(conf)
        connectionString = "mongodb://" + mongodbuser + ":" + mongodbpass + "@" + mongodbserver + ":27017/" + mongodblocation + "?retryWrites=true&w=majority"
        return connectionString, mongodbclustername, mongodbcollection

    def establishConnection():
        connectionString, mongodbclustername, mongodbcollection = DBOperations.mongofromConfig()
        cluster = MongoClient(connectionString)
        db = cluster[mongodbclustername]
        collection = db[mongodbcollection]
        return collection

    # Insert one post into MongoDB - uses whatever it is given so injection risk to worry about here
    def MongoInsertOne(post):
        collection.insert_one(post)

    # Need to read columns we care about from the DB and output as headers variable and variable with array of values
    def readData(self, columnstoget):
        distinctList = collection.distinct("clientAddress")
        allpostsforIP = collection.find({"clientAddress":clientAddress})

    # List columns to get
    def readCols():
        columns=[]
        firstpost = collection.find_one()
        for key, value in firstpost.items():
            columns.append(key)
        return columns
        
    # Ask user which columns to get
    def getCols():
        columns = DBOperations.readCols()
        columnstoget = []
        # Need a menu to allow the user to choose - TO DO: Add other paths so columnstoget can come from the command line or config file
        print("Which of the following columns should we collect?")
        itemnum = 0
        for item in columns:   # List all the columns for choice
            print(itemnum + ":" + item)
            itemnum += 1
        proceed = itemnum + 1
        print(proceed + ": Proceed with analysis using the column list above")
        iscrewup = proceed + 1
        print(iscrewedup + ": I made a mistake.  Note: This will hard exit the job and you will need to re-start completely.")
        if itemnum == iscrewup:  # Allow for mistakes since this is so simple a menu
            exit()
        while itemnum != proceed:  # Get as many columns as the user wants
            itemnum=input("Enter #")
            columnstoget.append(itemnum)
        return columnstoget

   
 # Main Method
def main():
    dboper=DBOperations.establishConnection()

    # Import data
    columnstoget = DBOperations.getCols()
    data = DBOperations.readData(columnstoget)
    print(data)

# Main execution

if __name__ == '__main__':
    main()