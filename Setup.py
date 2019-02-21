import csv
import os
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
with open('./SETUP/permission.csv','r',newline='') as f:
    reader = csv.DictReader(f)
    for i in reader:
        i['level_mng'] = int(i['level_mng'])
        i['user_mng'] = int(i['user_mng'])
        i['display_mode'] = int(i['display_mode'])
        i['ai_module'] = int(i['ai_module'])
        i['threshold'] = int(i['threshold'])
        i['el_gui'] = int(i['el_gui'])
        i['auto_manual'] = int(i['auto_manual'])
        i['shift_mng'] = int(i['shift_mng'])
        i['pic_upload'] = int(i['pic_upload'])
        try:
            AD = db.permission.find_one({"type" : i["type"]})
            if AD:
                  db.permission.replace_one({"type" : i["type"]},i)
            else:
                  db.permission.insert_one(i)
        except BaseException:
            pass
with open('./SETUP/user.csv','r',newline='') as f:
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

with open('./SETUP/el_config.csv','r',newline='') as f:
    reader = csv.DictReader(f)
    for i in reader:
        i['cell_amount'] = int(i['cell_amount'])
        i['display_mode'] = int(i['display_mode'])
        try:
            AD = db.el_config.find_one({"el_no" : i["el_no"]})
            if AD:
                  db.el_config.replace_one({"el_no" : i["el_no"]},i)
            else:
                  db.el_config.insert_one(i)
        except BaseException:
            pass
with open('./SETUP/gui_config.csv','r',newline='') as f:
    reader = csv.DictReader(f)
    #reader = csv.DictReader(f)
    for i in reader:
        #print(i['gui_no'])
        i['auto_time'] = int(i['auto_time'])
        i['manual_time'] = int(i['manual_time'])
        i['el_limit'] = int(i['el_limit'])
        try:
            AD = db.gui_setting.find_one({"gui_no" : i["gui_no"]})
            if AD:
                  db.gui_setting.replace_one({"gui_no" : i["gui_no"]},i)
            else:
                  db.gui_setting.insert_one(i)
        except BaseException:
            pass
with open('./SETUP/thresholds.csv','r',newline='') as f:
    reader = csv.DictReader(f)
    for i in reader:
        i['cr_size'] = int(i['cr_size'])
        i['cs_size'] = int(i['cs_size'])
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
