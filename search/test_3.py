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
barcode = '501478'
st = "2019-2-15 22:00:00"
start = time.mktime(time.strptime(st,"%Y-%m-%d %H:%M:%S"))
en = "2019-2-16 23:00:00"
end = time.mktime(time.strptime(en,"%Y-%m-%d %H:%M:%S"))
#for barcode in range(10):
    #ID = db.panel.find_one({"barcode":str(barcode)})
data = list(db.panel.find({'barcode':barcode}).sort([("_id" , -1)]).limit(1))
data[0]['defects']
defect = pd.DataFrame(data[0]['defects'])
#print(data)
defect.to_csv('%s.csv'%(barcode),encoding='utf-8')
#ID = list(db.panel.aggregate([{'$match':{'create_time':{'$gte':start,'$lt':end}}}]))

