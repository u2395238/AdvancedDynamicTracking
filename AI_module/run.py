from __future__ import print_function
import face_recognition
import cv2
import numpy as np
import time
import datetime
from imutils.video import FileVideoStream
from imutils.video import FPS
import imutils
import pymongo
import random

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mylog = mydb["log"]

myvisitsdb = myclient["myvisitsdb"]
my_global_log = myvisitsdb["myvisits"]

myglobaldb = myclient["mylastseendb"]
my_lastseen_log = myglobaldb["mylastseen"]




print("[INFO] sampling frames from webcam...")
video_capture = FileVideoStream("./video.mp4").start()
#time.sleep(1.0)
fps = FPS().start()


President_image = face_recognition.load_image_file("./known/President.jpg")
President_face_encoding = face_recognition.face_encodings(President_image)[0]

Agent2_image = face_recognition.load_image_file("./known/Agent2.jpg")
Agent2_face_encoding = face_recognition.face_encodings(Agent2_image)[0]

Agent1_image = face_recognition.load_image_file("./known/Agent1.jpg")
Agent1_face_encoding = face_recognition.face_encodings(Agent1_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    President_face_encoding,
    Agent2_face_encoding,
    Agent1_face_encoding
]
known_face_names = [
    "President",
    "Agent2",
    "Agent1"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

 
totalVisits=dict({ '_id':random.randint(0,9999999), 'Agent1':0, 'Agent2':0, 'President':0, 'Unknown':0})
people_lastseen = dict(
        {
            '_id':random.randint(0,9999999),

            "President": None,
       
            "Agent1": None,
        
            "Agent2": None,

             'Unknown': None

        }
)
prev_frame = {'Agent1':0, 'Agent2':0, 'President':0, 'Unknown':0}
cameras = list([])

startDate = str(datetime.date.today())

while True and video_capture.more():

    log = []
    log_dict = dict({'employeeid':'date':None, 'time':None, 'people':[], 'location':None, 'startDate': startDate,
        'present_frame':{'Agent1':0, 'Agent2':0, 'President':0, 'Unknown':0}})
        
    log_face_name = []


    frame = video_capture.read()

    
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]


   
    # Only process every other frame of video to save time
    if process_this_frame:

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        # for face_encoding not in face_encodings:

        for key,val in prev_frame.items():
            print("prev frame "+ key + " " + str(val))
        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            log_time = str(datetime.date.today())
            log_dict["date"]= str(datetime.date.today())
            log_dict["time"]= str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) + ":" + str(datetime.datetime.now().second)

            log.append(log_time)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"


            totalVisits['_id'] = random.randint(0,9999999)
            try:
                my_global_log.insert_one(totalVisits)
            except pymongo.errors.DuplicateKeyError:
                my_global_log.update_one({"_id": totalVisits["_id"]},{"$set":totalVisits})
            
            people_lastseen['_id'] = random.randint(0,9999999)
            try:
                my_lastseen_log.insert_one(people_lastseen)
            except pymongo.errors.DuplicateKeyError:
                my_lastseen_log.update_one({"_id": people_lastseen["_id"]},{"$set":people_lastseen})
            


            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
            log_dict["people"].append(name)
            people_lastseen[name] = log_dict["time"]

            print("check")
            log_dict['present_frame'][name] = log_dict['present_frame'][name] + 1
        
            print(name+ " -> "+
                "prev_frame[name]:"+ 
            str(prev_frame[name]) +
             " log_dict['present_frame'][name] :"+
             str(log_dict['present_frame'][name] )
             )

            if( prev_frame[name] < log_dict['present_frame'][name] ):
                print("ok")
                totalVisits[name] += 1


            people_lastseen[name]= "on " +  str(datetime.date.today()) + " at " +  str(datetime.datetime.now().hour) + ":" + str(datetime.datetime.now().minute) + ":" + str(datetime.datetime.now().second)
            
        log_face_name = face_names
    
        print("updated prev")
        prev_frame = log_dict['present_frame']
        for key,val in prev_frame.items():
            print("prev frame "+ key + " " + str(val))

        
        for key,val in totalVisits.items():
            print("Total visits "+ key + " " + str(val))
        



        log_dict["location"]= "Camera1"
        log_s = str(log)
        # print(log)
        for key, val in log_dict.items():
            print(key,val)
        print("*"*100)
        file.writelines(log_s+"\n")
        mylog.insert_one(log_dict)


    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
      
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        frame_face = frame[top:bottom,left:right]
        cv2.imwrite("./unknown/unknown"+str(top)+".jpg",frame_face)

        cv2.putText(frame, "Queue Size: {}".format(video_capture.Q.qsize()),
		(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


    cv2.imshow('Video', frame)


    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
    fps.update()
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# Release handle to the webcam
video_capture.stop()
#video_capture.release() #closes video file
cv2.destroyAllWindows()