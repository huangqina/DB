import pandas as pd
import csv
from con2 import connect2

c = connect2()
db = c['tttt']
data = pd.DataFrame(list(db.panel.aggregate([
    {'$project':{"_id":0}},{'$sort':({'barcode':1})},
    {'$lookup': {'from':"panel_defect","pipeline":[
         {'$lookup':{'from':"defect","localField":"defect_id",   "foreignField":"_id","as":"defect"}
         },{'$project':
         {"_id":0,"defect_id":0,"panel_id":0}},{'$project':{"defect":{"_id":0}}}],"as": "defects"}}])))
data.to_csv('./csv/panel_defects.csv',encoding='utf-8')