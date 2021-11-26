from __future__ import print_function
import face_recognition
import cv2
import numpy as np
import time
import datetime
from imutils.video import WebcamVideoStream
from imutils.video import FileVideoStream
from imutils.video import FPS
import argparse
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



# print(mydb.list_collection_names())


#print list of the _id values of the inserted documents:
# print(x.inserted_ids)


file = open("log.txt","wt")


print("[INFO] sampling frames from webcam...")
#video_capture = WebcamVideoStream(src=0).start()
video_capture = FileVideoStream("./video.mp4").start()
#time.sleep(1.0)
fps = FPS().start()

###video_capture = cv2.VideoCapture("./video.mp4")

# Load a sample picture and learn how to recognize it.
President_image = face_recognition.load_image_file("./known/President.jpg")
President_face_encoding = face_recognition.face_encodings(President_image)[0]

# Load a second sample picture and learn how to recognize it.
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
    log_dict = dict({'date':None, 'time':None, 'people':[], 'location':None, 'startDate': startDate,
        'present_frame':{'Agent1':0, 'Agent2':0, 'President':0, 'Unknown':0}})
        
    log_face_name = []
    # Grab a single frame of video
    frame = video_capture.read() #read from the video file, decode, and return

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
   
    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        # for face_encoding not in face_encodings:
        #     cv2.imwrite("./unknown/unknown.jpg",rgb_small_frame)
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
            

            # # If a match was found in     known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
            log_dict["people"].append(name)
            people_lastseen[name] = log_dict["time"]
            # for key,val in people_lastseen.items():
            #     if(val != None):
            #         print(key+ ":" + val)

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
            ######Adding unknown to folder
            #no_of_unknown=0
            #for face_name in face_names:
                    #if face_name == "Unknown":
                        #cv2.imwrite("./unknown/unknown.jpg",frame_face)
                        #face_encodings.append(face_encoding)
                        #face_names.append("Unknown"+str(no_of_unknown))
                        #no_of_unknown+=1
        log_face_name = face_names
        log = log + log_face_name
        print("updated prev")
        prev_frame = log_dict['present_frame']
        for key,val in prev_frame.items():
            print("prev frame "+ key + " " + str(val))

        
        for key,val in totalVisits.items():
            print("Total visits "+ key + " " + str(val))
        


        log.append("Camera2")
        log_dict["location"]= "Camera2"
        log_s = str(log)
        # print(log)
        for key, val in log_dict.items():
            print(key,val)
        print("*"*100)
        file.writelines(log_s+"\n")
        mylog.insert_one(log_dict)


    # try:
    #     # if(people_lastseen["Agent1"] != None):
    #     x = totalVisits
    #     y = people_lastseen
    #     my_global_log.insert_one(x)
    #     my_global_log.insert_one(y)
    # except pymongo.errors.DuplicateKeyError:
    #     pass


    # my_global_log.insert_one(totalVisits)

    # my_global_log.insert_one(people_lastseen)
    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        frame_face = frame[top:bottom,left:right]
        cv2.imwrite("./unknown/unknown"+str(top)+".jpg",frame_face)

        cv2.putText(frame, "Queue Size: {}".format(video_capture.Q.qsize()),
		(10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
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