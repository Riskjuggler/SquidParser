import pymongo
from pymongo import MongoClient
import time
from datetime import datetime, timedelta, date



cluster = MongoClient("mongodb://SquidReporter-rw:SquidReporter-pass!!!@192.168.40.251:27017/SquidReporter?retryWrites=true&w=majority")
db = cluster["SquidReporter"]
collection = db["DevCollection"]

timestamp=datetime.strptime(str(datetime.utcfromtimestamp(float(1591794630.029))), "%Y-%m-%d %H:%M:%S.%f")
print(timestamp)
print(type(timestamp))
datevalue=str(timestamp).split()
print(datevalue[0])



post={
"logTime" : timestamp,
"logDate" : datevalue[0]
# "duration" : arrayLine[1],
# "clientAddress" : arrayLine[2],
# "resultCode" : arrayLine[3],
# "siteBytes" : arrayLine[4],
# "callType" : arrayLine[5],
# "siteUrl" : arrayLine[6],
# "userId" : arrayLine[7],
# "hierarchyCode" : arrayLine[8],
# "timeDiff" : 0,
}

result = collection.insert_one(post)

# post = {"name": "tim", "score" : 3}
# post = {'callType': 'HIER_DIRECT/17.248.131.173', 'siteUrl': 'CONNECT', 'siteBytes': '0', 'resultCode': 'NONE/200', 'timeDiff': 0, 'duration': '344', 'hierarchyCode': '-', 'parentTimestamp': 0.0, 'logTime': '1588163441.147', 'clientAddress': '192.168.40.135', 'userId': 'api.apple-cloudkit.com:443'}
# post1 = {'callType': 'HIER_DIRECT/17.248.131.173', 'siteUrl': 'CONNECT', 'siteBytes': '0', 'resultCode': 'NONE/200', 'timeDiff': 0, 'duration': '344', 'hierarchyCode': '-', 'parentTimestamp': 0.0, 'logTime': '1588163445.147', 'clientAddress': '192.168.40.135', 'userId': 'api.apple-cloudkit.com:443'}

#collection.insert_many([post, post1])
# timeStampPrevious = 0
# results = collection.find()
# for result in results:
#     timeStampCurrent = result["logTime"]
#     print(timeStampPrevious, "is before ", timeStampCurrent)
#     timeStampPrevious = timeStampCurrent

# allposts = collection.find_one()
# for key, value in allposts.items():
#     print(key)

# ipList = ""

# for ipAddress in allposts:
#     newIP = ipAddress["clientAddress"]
#     print(newIP)

# for ipAddress in allposts:
#     newIP = ipAddress["clientAddress"]
#     print(newIP," : ",ipList)
#     if newIP not in ipList:
#         ipList2 = ipList + " " + newIP
#         ipList = ipList2
#         print("ipList is ",ipList)

# distinctList = collection.distinct("clientAddress")
# print("Distinct list", distinctList)

# for clientAddress in distinctList:
#     print(clientAddress)