from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, NotMasterError
#client = MongoClient('localhost')
#db = client.ttt
#task = db.i
#print(task.count())
def connect2():
    fd = open("./config2")
    line = fd.readline()
    try:
        while line:
            ip = list(line.strip().split(':'))
            count = 0
            client = MongoClient("mongodb://root:123456@%s:%i"%(ip[0],int(ip[1])), serverSelectionTimeoutMS=5)
            while True:
                try:
                    client.admin.command("ping")
                except ConnectionFailure:
                    count = count + 1
                else:
                    if client.is_primary:
                        return client
                    else: 
                        line = fd.readline()
                        slave = client
                        break
                if count == 5:
                    line = fd.readline()
                    break
    except BaseException:
        pass
    return slave
connect2()
