db.panel.aggregate([{'$unwind':'$status'},{$match:{'status.by':'OP'}},
   {"$group":{
        '_id' : '$status'
            ,
        'count':{"$sum":1}}}])