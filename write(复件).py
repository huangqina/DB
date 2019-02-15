import pandas as pd
import csv
from con2 import connect2

c = connect2()
db = c['tttt']
data = pd.DataFrame(list(db.panel.find('$project':{'_id':0})
data.to_csv('./csv/panel_defects.csv',encoding='utf-8')
