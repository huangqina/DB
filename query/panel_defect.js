db.panel.aggregate([
    {$project:{"_id":0}},
    {$lookup: {'from':"panel_defect","pipeline":[
         
         
         
         {'$lookup':{'from':"defect","localField":"defect_id",   "foreignField":"_id","as":"defect"}
         },{'$project':
         {"_id":0,"defect_id":0,"panel_id":0}},{'$project':{"defect":{"_id":0}}}],"as": "defects"}}])