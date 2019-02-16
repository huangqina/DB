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
st = "2019-2-15 22:00:00"
start = time.mktime(time.strptime(st,"%Y-%m-%d %H:%M:%S"))
en = "2019-2-16 23:00:00"
end = time.mktime(time.strptime(en,"%Y-%m-%d %H:%M:%S"))
#for barcode in range(10):
    #ID = db.panel.find_one({"barcode":str(barcode)})

data = list(db.panel.aggregate([{'$match':{'create_time':{'$gte':start,'$lt':end}}},{'$project':{'_id':0,'display_mode':0,'thresholds':0,'cell_shape':0,'cell_amount':0,'cell_type':0,'defects':0}}]))
for i in data:
	for j in i['status']:
		if j['by'] == 'OP': 
			i['result'] = j['result']
	del i['status']
data = pd.DataFrame(data)
#print(data)
data.to_csv('1.csv',encoding='utf-8')
#ID = list(db.panel.aggregate([{'$match':{'create_time':{'$gte':start,'$lt':end}}}]))

