import csv
from con2 import connect2


c = connect2()
db = c['tttt']
with open('permission.csv','r',newline='') as f:
    reader = csv.DictReader(f)
    for i in reader:
        try:
            db.permission.insert_one(i)
        except BaseException:
            pass

with open('user.csv','r',newline='') as f:
    reader = csv.DictReader(f)
    for i in reader:
        i['activate'] = int(1)
        try:
            db.user.insert_one(i)
        except BaseException:
            pass

with open('el_config.csv','r',newline='') as f:
    reader = csv.DictReader(f)
    for i in reader:
        try:
            db.el_config.insert_one(i)
        except BaseException:
            pass

with open('gui_config.csv','r',newline='') as f:
    reader = csv.DictReader(f)
    for i in reader:
        try:
            db.gui_setting.insert_one(i)
        except BaseException:
            pass

with open('thresholds.csv','r',newline='') as f:
    reader = csv.DictReader(f)
    for i in reader:
        try:
            db.thresholds.insert_one(i)
        except BaseException:
            pass