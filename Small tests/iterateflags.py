import sys, getopt
import time
from datetime import datetime, timedelta

#  Using getopt from https://docs.python.org/2/library/getopt.html
confignogood = True  # Only need to collect config if it's no good
dbload = False   # Only need to load DB if it's not already loaded
reportonly = False  # Normal is to load DB and report
timeDiff = 0
ipaddress = ""
date = datetime.today() # TO DO: Need to get today in MMDDYYYY format

try:
    optlist, args = getopt.getopt(sys.argv[1:], 'hcri:d:t:')
    print("Optlist : ", optlist)
    print("Args : ", args)
except getopt.GetoptError as err:
    print('No flags or parameters so executing the fully manual approach.')
    sys.exit(2)

for opt, arg in optlist:   
    if opt == "-h":
        print("There are 5 unique ways to execute SquidParser.py")
        sys.exit()
    elif optlist == "-c":
        confignogood = False
    elif opt == "-r":
        reportonly = True
    elif opt == "-d":  # Need to fix this to get parameters too
        date = arg 
    elif opt == "-t":  # Need to fix this to get parameters too
        timeDiff = arg
    elif opt == "-i":  # Need to fix this to get parameters too
        ipaddress = arg
print("Outputs : ",confignogood, reportonly, date, timeDiff, ipaddress) 
