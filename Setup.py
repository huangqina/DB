import csv
from con2 import connect2


c = connect2()
db = c['tttt']
'''with open('permission.csv','r',newline='') as f:
    reader = csv.DictReader(f)
    for i in reader:
        try:
            db.permission.insert_one(i)
        except BaseException:
            pass
'''
'''    try:
        AD = el_config.find_one({"el_no" : info["el_no"]})
        if AD:
            el_config.update({"el_no" : info["el_no"]},{'el_no':info["el_no"],'cell_type':info["cell_type"],'cell_amount':info['cell_amount'],'display_mode':info['display_mode'],'module_no':info['module_no'],'thresholds':dic})       
        else:
            el_config.insert({'el_no':info["el_no"],'cell_type':info["cell_type"],'cell_amount':info['cell_amount'],'display_mode':info['display_mode'],'module_no':info['module_no'],'thresholds':dic})
               
        log.insert({'user_id' : info["admin_name"], 'time': info['time'],'action':"el_%s_config_change{%s}"%(info["el_no"],info["admin_name"])})
        logger.info("el_%s_config_change{%s}"%(info["el_no"],info["admin_name"]))
        return jsonify(1),200
    except BaseException as e:
        return str(e),400'''
with open('permission.csv','r',newline='') as f:
    reader = csv.DictReader(f)
    for i in reader:
        try:
            AD = db.permission.find_one({"type" : i["type"]})
            if AD:
                  db.permission.replace_one({"type" : i["type"]},i)
            else:
                  db.permission.insert_one(i)
        except BaseException:
            pass
with open('user.csv','r',newline='') as f:
    reader = csv.DictReader(f)
    for i in reader:
        i['activate'] = int(1)
        try:
            AD = db.user.find_one({"user_name" : i["user_name"],'activate' : 1})
            if AD:
                  db.user.replace_one({"user_name" : i["user_name"],'activate' : 1},i)
            else:
                  db.user.insert_one(i)
        except BaseException:
            pass

with open('el_config.csv','r',newline='') as f:
    reader = csv.DictReader(f)
    for i in reader:
        try:
            AD = db.el_config.find_one({"el_no" : i["el_no"]})
            if AD:
                  db.el_config.replace_one({"el_no" : i["el_no"]},i)
            else:
                  db.el_config.insert_one(i)
        except BaseException:
            pass
with open('gui_config.csv','r',newline='') as f:
    reader = csv.DictReader(f)
    for i in reader:
        try:
            AD = db.gui_setting.find_one({"gui_no" : i["gui_no"]})
            if AD:
                  db.gui_setting.replace_one({"gui_no" : i["gui_no"]},i)
            else:
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
        try:
            AD = db.thresholds.find_one({"threshold_module" : i["threshold_module"]})
            if AD:
                  db.thresholds.replace_one({"threshold_module" : i["threshold_module"]},i)
            else:
                  db.thresholds.insert_one(i)
        except BaseException:
            pass
