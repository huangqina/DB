import pandas as pd
import csv
import time 
#from pymongo import MongoClient
#from pymongo.errors import ConnectionFailure, NotMasterError
from con2 import connect2


#client = MongoClient("mongodb://root:123456@192.168.2.40:27017")
c = connect2()
db = c['tttt']
data = []
data_miss = []
data_overkill = []
data_total = []
missrate = []
st = "2019-2-15 22:00:00"
start = time.mktime(time.strptime(st,"%Y-%m-%d %H:%M:%S"))
en = "2019-2-16 23:00:00"
end = time.mktime(time.strptime(en,"%Y-%m-%d %H:%M:%S"))
#for barcode in range(10):
    #ID = db.panel.find_one({"barcode":str(barcode)})

data_miss = list(db.panel.aggregate([{'$unwind':'$defects'},{'$match':{'create_time':{'$gte':start,'$lt':end},'defects.by':'AI','defects.status':'false'}},
   {"$group":{
        '_id' :{ '_id':'$_id','by':'$defects.by','barcode':'$barcode','el_no':'$el_no','create_time':'$create_time'}
            ,
        'miss':{"$sum":1}}},]))
data_total = list(db.panel.aggregate([{'$unwind':'$defects'},{'$match':{'create_time':{'$gte':start,'$lt':end },'defects.by':'AI'}},
   {"$group":{
        '_id' :{ '_id':'$_id','by':'$defects.by','barcode':'$barcode','el_no':'$el_no','create_time':'$create_time'}
            ,
        'total':{"$sum":1}}},]))
data_overkill = list(db.panel.aggregate([{'$unwind':'$defects'},{'$match':{'create_time':{'$gte':start,'$lt':end},'defects.by':'OP'}},
   {"$group":{
        '_id' :{ '_id':'$_id','by':'$defects.by','barcode':'$barcode','el_no':'$el_no','create_time':'$create_time'}
            ,
        'total':{"$sum":1}}},]))
for i in data_total:
	dict1 = i["_id"]
	dict1["AI_total"] = i['total']
	for j in data_miss:
		if j["_id"]["_id"] == i["_id"]['_id']:
			dict1["AI_miss"] = j['miss']
			data_miss.remove(j)
	for x in data_overkill:
		if x["_id"]["_id"] == i["_id"]['_id']:
			dict1["OP"] = x['total']
			data_overkill.remove(x)
	data.append(dict1)
		
data = pd.DataFrame(data)
#print(data)
data.to_csv('4.csv',encoding='utf-8')
#ID = list(db.panel.aggregate([{'$match':{'create_time':{'$gte':start,'$lt':end}}}]))

