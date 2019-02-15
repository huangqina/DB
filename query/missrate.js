db.panel.aggregate([{'$unwind':'$defects'},
   {"$group":{
        '_id' : '$defects.status'
            ,
        'count':{"$sum":1}}}])