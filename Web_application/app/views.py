# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request
from jinja2  import TemplateNotFound
import pymongo

# App modules
from app import app

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    try:
        f = open("app/log.txt","r")
        dateline = f.readline()
        startdate = dateline[19:30]
        startdate  = startdate .replace(", ","-")
        f.close()
        
        # LOG = tracker("app/log.txt", startdate)
        # LOG = LOG + tracker("app/log2.txt", startdate)
        
        print()
        print()
        # Detect the current page
        segment = get_segment( request )
        print("-"*100)
        # for item in LOG:
        #     print(item)
        totalVisitCount = 0
        for key, val in totalVisits.items():
            totalVisitCount += val
            # print(key,val)

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["mydatabase"]
        mylog = mydb["log"]

        LOG = []

        for x in mylog.find():
            # print(x)
            LOG.append(x)
        

        mydb = myclient["myvisitsdb"]
        mylog = mydb["myvisits"]

        totalVisitsArray = []
        visitCountTotal = 0

        for x in mylog.find():
            # print(totalVisitsArray)
            totalVisitsArray.append(x)
            
        # print(str(visitCountTotal) + "!!!!")
        flag =1 
        visits ={}
        for key, val in totalVisitsArray[len(totalVisitsArray)-1].items():
            if flag ==1:
                flag= 0
                continue

            visits[key] = val

            visitCountTotal += val

        # print(visitCountTotal)

        mydb = myclient["mylastseendb"]
        mylog = mydb["mylastseen"]

        lastseenarray = [] 
        for x in mylog.find():
            lastseenarray.append(x)

        flag =1 
        lastseen ={}
        for key, val in lastseenarray[len(lastseenarray)-1].items():
            if flag ==1:
                flag= 0
                continue

            lastseen[key] = val
            # print(str(key + " " + str(val) ))

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(  path, hi="Hello",log_global = LOG,totalVisits = visits, 
        cameras = cameras,totalVisitCount = visitCountTotal,segment=segment, lastseen  = lastseen)
    
    except TemplateNotFound:
        return render_template('page-404.html'), 404

def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
totalVisits=dict({'Agent1':0, 'Agent2':0, 'President':0})
people = list([])
cameras = list([])

