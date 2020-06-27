import pymongo
from pymongo import MongoClient


cluster = MongoClient("mongodb://SquidReporter-rw:SquidReporter-pass!!!@192.168.40.251:27017/SquidReporter?retryWrites=true&w=majority")
db = cluster["SquidReporter"]
collection = db["DevCollection"]

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

allposts = collection.find_one()
for key, value in allposts.items():
    print(key)

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