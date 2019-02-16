import pandas as pd
import csv
import time 
from con2 import connect2

c = connect2()
db = c['tttt']
data = []
st = "2019-2-14 00:00:00"
start = time.mktime(time.strptime(st,"%Y-%m-%d %H:%M:%S"))
en = "2019-2-14 23:00:00"
end = time.mktime(time.strptime(en,"%Y-%m-%d %H:%M:%S"))
#for barcode in range(10):
    #ID = db.panel.find_one({"barcode":str(barcode)})
ID = list(db.panel.aggregate([{'$match':{'create_time':{'$gte':0,'$lt':100}}}]))

for i in ID:
    I = list(db.panel.aggregate([  
    {'$match':{'_id':i['_id']}},
    {'$project':{"_id":0}},
    {'$lookup': {'from':"panel_defect","pipeline":[
        {'$match':{'panel_id':i['_id']}},
         {'$lookup':{'from':"defect","localField":"defect_id",   "foreignField":"_id","as":"defect"}
         },{'$project':
         {"_id":0,"defect_id":0,"panel_id":0}},{'$project':{"defect":{"_id":0}}}],"as": "defects"}}]))
    data.append(I)
print(data)
data = pd.DataFrame(data)
#print(data)
data.to_csv('./csv/panel_defects.csv',encoding='utf-8')
#ID = list(db.panel.aggregate([{'$match':{'create_time':{'$gte':start,'$lt':end}}}]))

