# -*- coding: utf-8 -*- 
from flask import Flask,abort
from flask import jsonify
#from flask import render_template
from flask import request
from flask_pymongo import PyMongo
#from flask_script import Manager
from con2 import connect2
import json
from flask_apscheduler import APScheduler
import logging
import sys
import logging.handlers
#logging.basicConfig(filename="./log",level = logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
 
# 文件日志
#file_handler = logging.FileHandler("test.log")
file_handler = logging.handlers.TimedRotatingFileHandler("log/log", when='D', interval=1, backupCount=30)
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式.
file_handler.suffix = "%Y-%m-%d_%H-%M.log"
# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值
 
# 为logger添加的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)
 
# 指定日志的最低输出级别，默认为WARN级别
logger.setLevel(logging.INFO)
 
# 输出不同级别的log

#logger.info('this is information')
#logger.warn('this is warning message')
#logger.error('this is error message')
#logger.fatal('this is fatal message, it is same as logger.critical')
#logger.critical('this is critical message')
 
# 2016-10-08 21:59:19,493 INFO    : this is information
# 2016-10-08 21:59:19,493 WARNING : this is warning message
# 2016-10-08 21:59:19,493 ERROR   : this is error message
# 2016-10-08 21:59:19,493 CRITICAL: this is fatal message, it is same as logger.critical
# 2016-10-08 21:59:19,493 CRITICAL: this is critical message
 
# 移除一些日志处理器
#logger.removeHandler(file_handler)

c = connect2()
#connect('ttt', host='mongodb://database:27017,database2:27017', replicaSet='rs', read_preference=ReadPreference.SECONDARY_PREFERRED)

#c = MongoClient('mongodb://0.0.0.0:27017')
#mongo = c.ttt
#conn = MongoReplicaSetClient("192.168.2.25:27017,192.168.2.25:27018", replicaset='rs')
db = c['tttt']
app = Flask(__name__)
def re():
    global c 
    c = connect2()
    global db
    db = c['tttt']
#app.config.update(
    #MONGO_URI='mongodb://127.0.0.1:27017/ttt',
    #MONGO_USERNAME='bjhee',
    #MONGO_PASSWORD='111111',
    #MONGO_REPLICA_SET='rs',
    #MONGO_READ_PREFERENCE='SECONDARY_PREFERRED',
    #SCHEDULER_API_ENABLED = True
#)
app.config['SCHEDULER_API_ENABLED'] = True
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.add_job(id = '1',func = re, trigger='interval', seconds=60)
scheduler.start()
#app.config['MONGO_DBNAME'] = 'ttt'
#app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017'  #如果部署在本上，其中ip地址可填127.0.0.1
#app.config['MONGO_DBNAME'] = 'ttt'
#mongo = PyMongo(app)
#manager = Manager(app)
#db.authenticate("root","123456") 
if c.is_primary:
    db.user.ensure_index([("user_name",1),("activate",1)],unique=True)
    db.permission.ensure_index([("type",1)],unique=True)
    db.gui_setting.ensure_index([("gui_no",1)],unique=True)
    db.panel.create_index([("barcode", 1)])
    db.el_config.ensure_index([("el_no",1)],unique=True)
    db.panel.ensure_index([("barcode",1),("create_time",1),("el_no",1)],unique=True)
    #db.panel.ensure_index([("Barcode", 1)])
#mongo.db.el
    db.panel_status.create_index([("time", 1)])
    db.panel_status.create_index([("panel_id", 1)]) 
    db.defect.create_index([("time", 1)])
    db.panel_defect.create_index([("panel_id", 1)])
    db.panel_defect.create_index([("defect_id", 1)])
@app.route('/', methods=['GET'])
def show():
  #t = i['Defects'][0]['Defect']
  return '<p>Hello!</p>'
  #return  '<p>ip:5000/user/add {"admin_name": str, "user_name": str, "user_pw": str, "time": float}</p><p>ip:5000/user/del {"admin_name": str, "user_name": str, "admin_pw": str, "time": float}</p><p>ip:5000/user/login {"type": int, "user_name": str, "user_pw": str, "time": float}</p><p>ip:5000/user/logout {"user_name": str, "time": float}</p><p>ip:5000/panel/add {"barcode": str, "cell_type": str, "cell_amount": int, "el_no": str, "display_mode": int, "module_no": int, "thresholds": dict, "create_time": float, "ai_result": int, "ai_defects": dict, "gui_result": int, "gui_defects": dict}</p><p>ip:5000/barcode/find {"barcode": str}    #post barcode</p><p>ip:5000/NG/find   [float, float]  #post time</p><p>ip:5000/OK/find  [float, float]     #post time</p><p>ip:5000/missrate/find   [float, float] #post time</p><p>ip:5000/overkillrate/find   [float, float]  #post time</p><p>ip:5000/defect/find   [float, float]  #post time</p>'
@app.route('/user/show',methods=['POST','GET'])
def user_show():
    user = db.user
    a = user.find({"activate":1},projection={"_id":0,"activate":0,"user_pw":0})
    b = list(a)
    return jsonify(b)
@app.route('/user/display',methods=['POST','GET'])
def user_display():
    user = db.user
    a = user.find({"activate":1},projection={"_id":0,"user_pw":0,"activate":0})
    b = list(a)
    res = {}
    res["users"] = b
    return jsonify(res)
@app.route('/user/add',methods=['POST'])
def add_user():
    user = db.user
    log = db.user_log
    data = request.data
    info = json.loads(data.decode('utf-8'))
    if not info["user_name"]:
        logger.error('user_name null')
        return 'user_name null',400
    if not info["user_pw"]:
        logger.error('user_pw null')
        return 'user_pw null',400
    try:
        AD = user.find_one({"user_name" : info["admin_name"],"activate" : 1})
        if AD:
            user.insert({"user_name" : info["user_name"],"user_pw" : info["user_pw"],"activate" : 1,"type":info["type"]})
            log.insert({'admin_id' : AD["_id"],'admin_name' : info["admin_name"], 'time': info['time'],'action':"%s_add_user_%s"%(info["admin_name"],info["user_name"])})
            logger.info("user_add{%s}"%(info["user_name"]))
            return jsonify(1),200
        else:
            logger.error("admin user:%s didn't exist"%(info["admin_name"]))
            return jsonify("admin user didn't exist"), 400
    except BaseException as e:
        logger.error(str(e))
        return str(e),400
@app.route('/user/delete',methods=['POST'])
def del_user():
    user = db.user
    log = db.user_log
    data = request.data
    info = json.loads(data.decode('utf-8'))
    try:
        AD = user.find_one({"user_name" : info["admin_name"],"activate" : 1})
        if AD:
            I = user.find_one({"user_name" : info["user_name"]})
            I["activate"] = 0
            user.update({"user_name" : info["user_name"]},I)
            log.insert({'user_id' : I['_id'],'admin_id' : AD['_id'],'admin_name' : info["admin_name"], 'time': info['time'],'action':"%s_del_user_%s"%(info["admin_name"],info["user_name"])})
            logger.info("user_del_%s"%(info["user_name"]))
            return jsonify(1),200
        else:
            logger.error("admin user:%s didn't exist"%(info["admin_name"]))
            return jsonify("admin user didn't exist"), 400
    except BaseException as e:
        logger.error(str(e))
        return str(e),400
@app.route('/user/modify',methods=['POST'])
def user_modify():
    user = db.user
    log = db.user_log
    data = request.data
    info = json.loads(data.decode('utf-8'))
    change_list = []
    try:
        I = user.find_one({"user_name" : info["user_name"],"activate" : 1})
        if I:
            AD = user.find_one({"user_name" : info["admin_name"],"activate" : 1})
            #I = user.find_one({"user_name" : info["user_name"],"activate" : 1})
            for i in info["changed_items"].keys():
                if not info["changed_items"][i]:
                    logger.error("user_change is null")
                    return 'user_change is null',400
                I[i] = info["changed_items"][i]
                change_list.append(i)
            changes = '_'.join(change_list) 
            user.update({"_id" : I["_id"],"activate" : 1},I)
            log.insert({'admin_id' : AD['_id'],'user_name' : info['user_name'],'user_id' : I['_id'],'admin_name' : info["admin_name"], 'time': info['time'],'action':"%s_change_user:%s_%s"%(info["admin_name"],info["user_name"],changes)})
            logger.info("user_modify_%s"%(info["user_name"]))
            return jsonify(1),200
        else:
            logger.error("user:%s didn't exist"%(info["admin_name"]))
            return jsonify("user didn't exist"), 422
    except BaseException as e:
        logger.error(str(e))
        return str(e),400
@app.route('/user/password/change',methods=['POST'])
def user_password_change():
    user = db.user
    log = db.user_log
    data = request.data
    info = json.loads(data.decode('utf-8'))
    try:
        AD = user.find_one({"name" : info["admin_name"],"activate" : 1})
        if AD:
            I = user.find_one({"name" : info["user_name"],"activate" : 1})
            I["pw"] = info["user_pw"]
            user.update({"name" : info["user_name"],"activate" : 1},I)
            log.insert({'user_id' : AD['_id'],'user_name' : info["admin_name"], 'time': info['time'],'action':"%s_password_change{%s}"%(info["admin_name"],info["user_name"])})
            logger.info("password_change{%s}"%(info["user_name"]))
            return jsonify(1),200
    except BaseException as e:
        return str(e),400
@app.route('/user/login/operator',methods=['POST'])
def login_operator():
    user = db.user
    log = db.user_log
    data = request.data
    info = json.loads(data.decode('utf-8'))
    I = user.find_one({"user_name" : info["user_name"],"user_pw" : info["user_pw"],"activate" : 1})
    
    if  I:
        log.insert({'user_id' : I['_id'], 'user_name' : info["user_name"], 'time': info['time'],'action':"login_%s"%(info["user_name"])})
        #return str(int(I["type"])),200
        logger.info("login_%s"%(info["user_name"]))
        return jsonify(I["type"]),200
    else:
        logger.error("user:%s didn't exist"%(info["user_name"]))
        return jsonify("user didn't exist"), 400
@app.route('/user/login/admin',methods=['POST','GET'])
def login_admin():
    user = db.user
    permission = db.permission
    el_config = db.el_config
    gui_setting = db.gui_setting
    thresholds = db.thresholds
    log = db.user_log
    data = request.data
    info = json.loads(data.decode('utf-8'))
    result = {}
    try:
        I = user.find_one({"user_name" : info["user_name"],"user_pw" : info["user_pw"],"activate" : 1})
        if  I:
            log.insert({'user_id' : I['_id'], 'user_name' : info["user_name"], 'time': info['time'],'action':"login_%s"%(info["user_name"])})
            #return str(int(I["type"])),200
            logger.info("login_%s"%(info["user_name"]))
            result["type"] = I["type"]
            P = permission.find(projection={"_id":0})
            result["permission_mng"] = list(P)
            E = el_config.find(projection={"_id":0})
            result["line_setting"] = list(E)
            G = gui_setting.find(projection={"_id":0})
            result["gui_setting"] = list(G)
            T = thresholds.find(projection={"_id":0})
            result["thresholds"] = list(T)
            logger.info("admin_login_%s"%(info["user_name"]))
            return jsonify(result), 200
        else:
            logger.error("user:%s didn't exist"%(info["user_name"]))
            return jsonify("user didn't exist"), 421
    except BaseException:
        return jsonify("error"), 400
@app.route('/user/logout',methods=['POST'])
def logout():
    user = db.user
    log = db.user_log
    data = request.data
    info = json.loads(data.decode('utf-8'))
    I = user.find_one({"name" : info["user_name"],"activate" : 1})
    if  I:
        log.insert({'user_id' : I['_id'], 'user_name' : info["user_name"], 'time': info['time'],'action':"logout_%s"%(info["user_name"])})
        logger.info("logout_%s"%(info["user_name"]))
        return jsonify(1),200
    else:
        logger.error("user:%s didn't exist"%(info["user_name"]))
        return "user didn't exist", 400
@app.route('/el/config/modify',methods=['POST'])
def el_config_change():
    el_config = db.el_config
    user = db.user
    log = db.user_log
    data = request.data
    change_list = []
    info = json.loads(data.decode('utf-8'))
    try:
        EL = el_config.find_one({"el_no" : info["el_no"]})
        AD = user.find_one({"user_name" : info["admin_name"],"activate" : 1})
        if EL:
            for i in info["changed_items"].keys():
                EL[i] = info["changed_items"][i]
                change_list.append(i)
            changes = '_'.join(change_list) 
            el_config.update({"el_no" : info["el_no"]},EL)
            log.insert({'admin_id' : AD['_id'],'admin_name' : info["admin_name"],'el_id' : EL['_id'],'el_no' : info["el_no"], 'time': info['time'],'action':"%s_change_el_config:%s_%s"%(info["admin_name"],info["el_no"],changes)})
            logger.info('el_config_modify')
            return jsonify(1),200
        else:
            logger.error("el_no:%s didn't exist"%(info["admin_name"]))
            return jsonify("el_no didn't exist"), 422
    except BaseException as e:
        logger.error(str(e))
        return str(e),400
@app.route('/gui/config/modify',methods=['POST'])
def gui_config_modify():
    gui_setting = db.gui_setting
    user = db.user
    log = db.user_log
    data = request.data
    change_list = []
    info = json.loads(data.decode('utf-8'))
    try:
        GUI = gui_setting.find_one({"gui_no" : info["gui_no"]})
        AD = user.find_one({"user_name" : info["admin_name"],"activate" : 1})
        if GUI:
            for i in info["changed_items"].keys():
                GUI[i] = info["changed_items"][i]
                change_list.append(i)
            changes = '_'.join(change_list) 
            gui_setting.update({"gui_no" : info["gui_no"]},GUI)
            log.insert({'admin_id' : AD['_id'],'admin_name' : info["admin_name"],'gui_id' : GUI['_id'],'gui_no' : info["gui_no"], 'time': info['time'],'action':"%s_change_gui_config:%s_%s"%(info["admin_name"],info["gui_no"],changes)})
            logger.info('gui_config_modify')
            return jsonify(1),200
        else:
            logger.error("gui_no:%s didn't exist"%(info["admin_name"]))
            return jsonify("gui_no didn't exist"), 422
    except BaseException as e:
        logger.error(str(e))
        return str(e),400
@app.route('/permission/modify',methods=['POST'])
def permission_modify():
    permission = db.permission
    user = db.user
    log = db.user_log
    data = request.data
    change_list = []
    info = json.loads(data.decode('utf-8'))
    AD = user.find_one({"user_name" : info["admin_name"],"activate" : 1})
    try:
        for i in info["changed_items"]:
            P = permission.find_one({"type" : i["type"]})
            if P:
                for j in i.keys():
                    P[j] = i[j]
                    change_list.append(j)
                changes = '_'.join(change_list) 
                permission.update({"type" : i["type"]},P)
                log.insert({'admin_id' : AD['_id'],'admin_name' : info["admin_name"],'type_id' : P['_id'],'type' : i["type"], 'time': info['time'],    'action':"%s_change_permission_config:%s_%s"%(info["admin_name"],i["type"],changes)})
                logger.info('permission_modify')
            else:
                 logger.error("type:%s didn't exist"%(i["type"]))
                 return jsonify("type didn't exist"), 422
        return jsonify(1),200
    except BaseException as e:
        logger.error(str(e))
        return str(e),400
    '''try:
        P = permission.find_one({"type" : info["type"]})
        AD = user.find_one({"user_name" : info["admin_name"],"activate" : 1})
        if P:
            for i in info["changed_items"].keys():
                P[i] = info["changed_items"][i]
                change_list.append(i)
            changes = '_'.join(change_list) 
            permission.update({"type" : info["type"]},P)
            log.insert({'admin_id' : AD['_id'],'admin_name' : info["admin_name"],'type_id' : P['_id'],'type' : info["type"], 'time': info['time'],'action':"%s_change_permission_config:%s_%s"%(info["admin_name"],info["type"],changes)})
            logger.info('permission_modify')
            return jsonify(1),200
        else:
             logger.error("type:%s didn't exist"%(info["admin_name"]))
             return jsonify("type didn't exist"), 422
    except BaseException as e:
        logger.error(str(e))
        return str(e),400'''
'''@app.route('/el/config/change',methods=['POST'])
def el_config_change():
    el_config = db.el_config
    log = db.user_log
    data = request.data
    dic = {}
    info = json.loads(data.decode('utf-8'))
    try:
        if info['thresholds']:
            for k in info['thresholds'].keys():
                dic[k] = info['thresholds'][k]
    except BaseException:
        pass 
    try:
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
@app.route('/el/config/display',methods=['POST','GET'])
def el_config_display():
    el_config = db.el_config
    #log = db.user_log
    #data = request.data
    #info = json.loads(data.decode('utf-8'))
    #try:
        #log.insert({'user_id' : info["admin_name"], 'time': info['time'],'action':"el_%s_config_change{%s}"%(info["el_no"],info["admin_name"])})
    a = el_config.find(projection={"_id":0})
    b = list(a)
    logger.info('el_config_display')
    return jsonify(b)
#@app.route('/el/config/check',methods=['POST'])
#def el_config_check():
@app.route('/el/config/check',methods=['POST','GET'])
def el_config_check():
    el_config = db.el_config
    data = request.data
    info = json.loads(data.decode('utf-8'))
    #log = db.user_log
    #data = request.data
    #info = json.loads(data.decode('utf-8'))
    #try:
        #log.insert({'user_id' : info["admin_name"], 'time': info['time'],'action':"el_%s_config_change{%s}"%(info["el_no"],info["admin_name"])})
    try:
        AD = el_config.find_one({"el_no" : info["el_no"]},projection={"_id":0})
        if not AD:
            return 'null',400
        logger.info('el_config_check')
        return jsonify(AD),200
    except BaseException as e:
        logger.error(str(e))
        return str(e),400
@app.route('/gui/config/check',methods=['POST','GET'])
def gui_config_check():
    gui_setting = db.gui_setting
    data = request.data
    info = json.loads(data.decode('utf-8'))
    #log = db.user_log
    #data = request.data
    #info = json.loads(data.decode('utf-8'))
    #try:
        #log.insert({'user_id' : info["admin_name"], 'time': info['time'],'action':"el_%s_config_change{%s}"%(info["el_no"],info["admin_name"])})
    try:
        AD = gui_setting.find_one({"gui_no" : info["gui_no"]},projection={"_id":0})
        if not AD:
            return 'null',400
        logger.info('gui_config_check')
        return jsonify(AD),200
    except BaseException as e:
        logger.error(str(e))
        return str(e),400
#@app.route('/el/config/check',methods=['POST'])
#def el_config_check():
@app.route('/panel/add',methods=['POST'])
def panel_add():
    #display_mode = db.display_mode
    #module_no = db.module_no
    thresholds = db.thresholds
    PANEL = db.panel
    EL = db.el
    PANEL_STATUS = db.panel_status 
    DEFECT = db.defect 
    PANEL_DEFECT = db.panel_defect 
    #AI = mongo.db.ai 
    data = request.data
    info = json.loads(data.decode('utf-8'))
    try:
        if not isinstance(info['barcode'],str):
            logger.error('barcode should be str')
            #raise TypeError("barcode should be str")
            return 'barcode should be str',400
        if info['cell_type'] not in ['mono','poly']:
            #   raise TypeError('cell_type wrong')
            logger.error('cell_type wrong')
            return 'cell_type wrong',400
        #if info['cell_size'] not in ['half','full']:
            #raise TypeError('cell_size wrong')
            #logger.error('cell_size wrong')
            #return 'cell_size wrong',400
        if info['cell_amount'] not in [60,72,120,144]:
            #raise TypeError('cell_amount wrong')
            logger.error('cell_amount wrong')
            return 'cell_amount wrong',400
        if not isinstance(info['el_no'],str):
            #raise TypeError('el_no should be str')
            logger.error('el_no should be str')
            return 'el_no should be str',400
        if not isinstance(info['create_time'],float):
            logger.error('create_time should be float')
            return 'create_time should be float',400
        if info['display_mode'] not in [0,1,2]:
            #raise TypeError('ai_result should be 0 or 1')
            logger.error('display_mode should be 0 or 1 or 2')
            return 'ai_result should be 0 or 1 or 2',400
        if info['ai_result'] not in [0,1,2]:
            #raise TypeError('ai_result should be 0 or 1')
            logger.error('ai_result should be 0 or 1 or 2')
            return 'ai_result should be 0 or 1 or 2',400
        if not isinstance(info['ai_defects'], dict):
            #raise TypeError('ai_defects should be list')
            logger.error('ai_defects should be dict')
            return 'ai_defects should be dict',400
        if info['ai_defects']:
            for k in info['ai_defects'].keys():
                if k not in ['cr','cs','bc','mr']:
                    #raise TypeError('ai_defects wrong')
                    logger.error('ai_defects wrong')
                    return 'ai_defects wrong',400
        #if not isinstance(info['ai_time'],float):
            #logger.error('ai_time should be float')
            #return 'ai_time should be float',400
        if info['gui_result'] not in [0,1,2]:
            #raise TypeError('gui_result should be 0 or 1')
            logger.error('gui_result should be 0 or 1')
            return 'gui_result should be 0 or 1',400
        if not isinstance(info['gui_defects'], dict):
            #raise TypeError('gui_defects should be list')
            logger.error('gui_defects should be dict')
            return 'gui_defects should be dict',400
        if info['gui_defects']:
            for k in info['gui_defects'].keys():
                if k not in ['cr','cs','bc','mr']:
                    #raise TypeError('gui_defects wrong')
                    logger.error('gui_defects wrong')
                    return 'gui_defects wrong',400     
        #if not isinstance(info['gui_time'],float):
            #logger.error('gui_time should be float')
            #return 'gui_time should be float',400
    except BaseException as e:
        logger.error('json file error  '+str(e))
       
        return str('json file error  '+str(e)),400
    defects = []
    status = []
    status.append({'result':info['ai_result'],'by':'AI'})
    status.append({'result':info['gui_result'],'by':'OP'})
    if info['ai_defects']:
        for k in info['ai_defects'].keys():
            for v in info['ai_defects'][k]:
                if info['gui_defects'][k] and v in info['gui_defects'][k]:
                    defects.append({'type':k,'position':v,'by':'AI','status':'true'})
                    #PANEL_DEFECT.insert({'panel_id':panel_id,'defect_id':defect_id,'by':'AI','status':'true'})
                    defects.append({'type':k,'position':v,'by':'OP','status':'true'})
                    info['gui_defects'][k].remove(v)
                elif not info['gui_defects'][k] or (info['gui_defects'][k] and v not in info['gui_defects'][k]):
                    defects.append({'type':k,'position':v,'by':'AI','status':'false'})
                    #PANEL_DEFECT.insert({'panel_id':panel_id,'defect_id':defect_id,'by':'AI','status':'false'})
    if info['gui_defects']:
        for k in info['gui_defects'].keys():
            if info['gui_defects'][k]:
                for v in info['gui_defects'][k]:
                    defects.append({'type':k,'position':v,'by':'OP','status':'true'})
                    #PANEL_DEFECT.insert({'panel_id':panel_id,'defect_id':defect_id,'by':'OP','status':'true'})
    dic = {}
    try:
        if info['thresholds']:
            for k in info['thresholds'].keys():
                dic[k] = info['thresholds'][k]
    except BaseException:
        pass
    try:
        PANEL.insert({'barcode' : info['barcode'], 'cell_type': info['cell_type'],'cell_amount': info['cell_amount'],'cell_shape':info['cell_shape'],'display_mode': info['display_mode'],'el_no':info['el_no'],'create_time':info['create_time'],'defects':defects,'status':status,'thresholds':dic})
    except BaseException as e:
        logger.error('barcode already exists')
        return str(e),400
    #display_mode.insert({'display_mode': info['display_mode']})
    #module_no.insert({'module_no': info['module_no']})
    EL.insert({'el_no': info['el_no']})
    '''try:
        panel_id = PANEL.insert({'barcode' : info['barcode'], 'cell_type': info['cell_type'],'cell_amount': info['cell_amount'],'cell_shape':info['cell_shape'],'display_mode': info['display_mode'],'el_no':info['el_no'],'create_time':info['create_time']})
    except BaseException as e:
        logger.error('barcode already exits')
        return str(e),400
    #display_mode.insert({'display_mode': info['display_mode']})
    #module_no.insert({'module_no': info['module_no']})
    dic = {}
    try:
        if info['thresholds']:
            for k in info['thresholds'].keys():
                dic[k] = info['thresholds'][k]
            thresholds.insert(dic)
    except BaseException:
        pass
    EL.insert({'el_no': info['el_no']})
    #panel = PANEL.find_one({'_id': panel_id })
    PANEL_STATUS.insert({'panel_id':panel_id,'time':info['create_time'],'result':info['ai_result'],'by':'AI'})
    PANEL_STATUS.insert({'panel_id':panel_id,'time':info['create_time'],'result':info['gui_result'],'by':'OP'})
    if info['ai_defects']:
        for k in info['ai_defects'].keys():
            for v in info['ai_defects'][k]:
                if info['gui_defects'][k] and v in info['gui_defects'][k]:
                    defect_id = DEFECT.insert({'type':k,'position':v,'by':'AI','time':info['create_time']})
                    PANEL_DEFECT.insert({'panel_id':panel_id,'defect_id':defect_id,'by':'AI','status':'true'})
                    info['gui_defects'][k].remove(v)
                elif info['gui_defects'][k] and v not in info['gui_defects'][k]:
                    defect_id = DEFECT.insert({'type':k,'position':v,'by':'AI','time':info['create_time']})
                    PANEL_DEFECT.insert({'panel_id':panel_id,'defect_id':defect_id,'by':'AI','status':'false'})
    if info['gui_defects']:
        for k in info['gui_defects'].keys():
            if info['gui_defects'][k]:
                for v in info['gui_defects'][k]:
                    defect_id = DEFECT.insert({'type':k,'position':v,'by':'OP','time':info['create_time']})
                    PANEL_DEFECT.insert({'panel_id':panel_id,'defect_id':defect_id,'by':'OP','status':'true'})'''
    logger.info('add panel')
    return jsonify(1),200
    #return 'OK',200
@app.route('/barcde/find', methods=['GET','POST'])
def barcde_find(): 
    #user = db.users 
    collection = db.panel
    data = request.data
    Barcode = json.loads(data.decode('utf-8'))
    Barcode = Barcode["barcode"]
    #Barcode = request.args['Barcode']
    I = list(db.panel.aggregate([{'$match':{'barcode':Barcode}},{'$project':{'_id':0,'thresholds':0}}]))
    '''I = list(db.panel.find({"barcode" : Barcode}).limit(1).sort([("_id" , -1)]))'''
    '''if I:
        ID = I[0]['_id']
    else: 
        ID = -1'''
    #username = user.find_one({"username":username}) 
    #if username: 
    #    return "你查找的用户名：" + username["username"] + " 密码是：" + username["password"] 
    #else: 
    #    return "你查找的用户并不存在!" 
    '''k = list(collection.aggregate([
    
    {'$match':{"_id":ID}},
    {'$project':{"_id":0}},
    {'$lookup': {'from':"panel_defect","pipeline":[
         
         {'$match':{ "panel_id": ID }},
         
         {'$lookup':{'from':"defect","localField":"defect_id",   "foreignField":"_id","as":"defect"}
         },{'$project':
         {"_id":0,"defect_id":0,"panel_id":0}},{'$project':{"defect":{"_id":0}}}],"as": "defects"}}]))'''
   # a=str('ID:'+str(k[0]['ID'])+'  '+'Barcode:' + str(k[0]['Barcode'])+'  '+'type:'+str(k[0]['type'])+'  '+ 'size:'+ str(k[0]['size']) +'  '+'EL_no:'+ str(k[0]['EL_no']))

    #return str(a)+'\n'+str(k[0]['Defects'])
    #return str(k[0]['Defects'])
    return jsonify(I[0])
    # for i in k['Defects']:
          #  print(i['Defect'])
@app.route('/panel/check_last', methods=['GET','POST'])
def check_last():
    panel = db.panel
    data = request.data
    info = json.loads(data.decode('utf-8'))
    #Barcode = request.args['Barcode']
    I = panel.find_one({"barcode" : info["barcode"],"create_time" : info["create_time"]}) 
    if I:
        return jsonify(1)
    else:
        return jsonify(0)
@app.route('/OK/find', methods=['GET','POST']) 
def findOK(): 
    data = request.data
    time = json.loads(data.decode('utf-8'))
    #start = float(request.args['start'])
    #end = float(request.args['end'])
    #start = str(time[0])
    #end = str(time[1])
    start = time[0]
    end = time[1]
    a=list(db.panel_status.aggregate([
    {"$match":{'time':{"$gt":start,"$lt":end}}},
    {"$group":{
        '_id' : "$result"
            ,
        'count':{"$sum":1}}}
    ]
    ))
    return jsonify(a)
   # '''
    #if a:
   #     return str('OK'+':'+str(a[0]['count'])+' '+'Defect'+':'+str(a[1]['count']))
    #else:
   #     return 'False'
   # '''
@app.route('/NG/find', methods=['GET','POST']) 
def findNG(): 
    data = request.data
    time = json.loads(data.decode('utf-8'))
    #start = float(request.args['start'])
    #end = float(request.args['end'])
    #start = str(time[0])
    #end = str(time[1])
    start = time[0]
    end = time[1]
    #start = float(request.args['start'])
    #end = float(request.args['end'])
    a=list(db.panel_status.aggregate([
    {"$match":{'time':{"$gt":start,"$lt":end}}},
    {
    "$group":{
        '_id' : "$result"
            ,
        'count':{"$sum":1}}}
    ]
    ))
    return jsonify(a)
    '''
    if a:
        return str('OK'+':'+str(a[0]['count'])+' '+'Defect'+':'+str(a[1]['count']))
    else:
        return 'False'
    '''
@app.route('/missrate/find', methods=['GET','POST']) 
def missrate(): 
    data = request.data
    time = json.loads(data.decode('utf-8'))
   # start = int(request.args['start'])
   # end = int(request.args['end'])
    start = time[0]
    end = time[1]
    k = list(db.defect.aggregate([
    
    {"$match":{'time':{"$gt":start,"$lt":end}}},
    {'$project':{"_id":1}},
    {'$lookup':{'from':'panel_defect',"localField":"_id",   "foreignField":"defect_id","as":"defect"}
         },{'$project':{"defect":
         {"_id":0,"defect_id":0,"panel_id":0}}},{'$project':{"_id":0}},{
    "$group":{
        '_id' : "$defect.by"
            ,
        'count':{"$sum":1}}}]))
    #a=list(mongo.db.panel_defect.aggregate([
    #{'$match':{'time':{'$gt':start,'$lt':end}}},
    #{
    #'$group':{
    #    '_id' : "$by"
    #        ,
    #    'count':{'$sum':1}}}
    #]
    #))
    return jsonify(k)
    #return jsonify(a[0]['count']/(a[1]['count']+a[0]['count']))

@app.route('/overkillrate/find', methods=['GET','POST']) 
def overkillrate(): 
   # start = int(request.args['start'])
   # end = int(request.args['end'])
    #{'$match':{'time':{'$gt':start,'$lt':end}}},
    #start = float(request.args['start'])
    #end = float(request.args['end'])
    data = request.data
    time = json.loads(data.decode('utf-8'))
   # start = int(request.args['start'])
   # end = int(request.args['end'])
    start = time[0]
    end = time[1]
    k = list(db.defect.aggregate([
    
    {"$match":{'time':{"$gt":start,"$lt":end}}},
    {'$project':{"_id":1}},
    {'$lookup':{'from':'panel_defect',"localField":"_id",   "foreignField":"defect_id","as":"defect"}
         },{'$project':{"defect":
         {"_id":0,"defect_id":0,"panel_id":0}}},{'$project':{"_id":0}},{
    "$group":{
        '_id' : "$defect.status"
            ,
        'count':{"$sum":1}}}]))
    '''
    if a:
        return str(a)
    else:
        return 'None'
    '''
    return jsonify(k)
    #return str(a[1]['count']/(a[1]['count']+a[0]['count']))
@app.route('/defect/find', methods=['GET','POST']) 
def defecttime(): 
   # start = int(request.args['start'])
   # end = int(request.args['end'])
    data = request.data
    time = json.loads(data.decode('utf-8'))
   # start = int(request.args['start'])
   # end = int(request.args['end'])
    start = time[0]
    end = time[1]
    k = list(db.defect.aggregate([
    
    {"$match":{'time':{"$gt":start,"$lt":end}}},
    {'$project':{"_id":1}},
    {'$lookup':{'from':'panel_defect',"localField":"_id",   "foreignField":"defect_id","as":"defect"}
         },{'$project':{"defect":
         {"_id":0,"defect_ID":0,"panel_id":0}}},{'$project':{"_id":0}},{
    "$group":{
        '_id' : "$defect.status"
            ,
        'count':{"$sum":1}}}]))
    '''
    if a:
        return str(a)
    else:
        return 'None'
    '''
    return jsonify(k)
if __name__ == '__main__':

    # app.run(host = '0.0.0.0', por)t = 80, debug = True)
    app.run(host = '0.0.0.0', port = 5001, debug = True)
