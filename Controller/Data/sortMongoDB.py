from datetime import datetime
import pymongo
globalTimeList:list = []

def getBaseDataFromMongoDB():
     global  globalTimeList
     client = pymongo.MongoClient(host='localhost', port=27017)
     db = client.drillProject
     for coll in db.list_collection_names():
          globalTimeList.append(coll)
     globalTimeList.sort(key=lambda date: datetime.strptime(date, "%m月%d日"))
     print(globalTimeList)

getBaseDataFromMongoDB()
print(globalTimeList)