db.panel.aggregate([{'$unwind':'$defects'},{'$match':{'defects.by':'AI'}},
   {"$group":{
        '_id' :{ 'by':'$defects.by','status':'$defects.status'}
            ,
        'count':{"$sum":1}}}])