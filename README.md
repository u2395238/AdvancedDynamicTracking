# ADVANCED DYNAMIC TRACKING (ADT)

## 1. INTRODUCTION 
![Capture-7](https://user-images.githubusercontent.com/49821723/181609483-bbdb7101-d04a-44fe-b1ce-e8fbdc568ad1.PNG)
<p align="center">Fig 1 ADT system</p>

### 1.1 Purpose 

In our proposed solution we focus on developing a system that dynamically tracks movements in a given area using camera and triggering necessary actions, this solution implements object tracking in computer vision over a network of cameras generating geofences with occupancy map allowing the system to track movements of individuals, traffic and objects across any area with attention to features such as direction of motion, velocity, physical appearance etc. This would allow us to leverage the best of multivariate data. We developed a user interface that detects the malicious movements in the area via the surveillance network. It differentiates the legitimate movements from the malicious movements and aims in regulating unauthorized movement.  It is used by security administrators to monitor the area.

## 2. OVERALL DESCRIPTION 

### 2.1 Product Perspective 


### 2.2 Product Functions

#### 2.2.1 Adding or removing authorized personnel

The surveillance administrator is an authority that has exclusive access to the system as a whole and can add or remove authorized personnel from the surveillance system. This process is as simple as adding a few demographics from the user interface and feeding it to the system which then recognizes the person across the area of interest.

#### 2.2.3 Tracking

The purpose of the system to recognize and identify people is coupled with tracking appropriate movements.


### 2.3 Operating Environment 

Hardware: Surveillance system network over the entire area with cameras supporting 60 fps video streaming.
Database: MongoDB is a document database, which means it stores data in JSON-like documents. We believe this is the most natural way to think about data, and is much more expressive and powerful than the traditional row/column model.
Operating system: Linux is a family of open-source Unix-like operating systems based on the Linux kernel, an operating system kernel 

## 3. EXTERNAL INTERFACE REQUIREMENTS

### 3.1 User Interfaces 

It provides the list of authorized personnel, frequency of motion, geofences and analytics.

### 3.2 Software Interfaces 

**Python 3.6**: Python is an interpreted, object-oriented, high-level programming language with dynamic semantics. Its high-level built-in data structures, combined with dynamic typing and dynamic binding, make it very attractive for Rapid Application Development, as well as for use as a scripting or glue language to connect existing components together. 

**Flask**: Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries. It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. 

**Face recognition**: The ‘face_recognition’ library recognizes and manipulates faces from Python or from the command line with the world’s simplest face recognition library. Built using dlib’s state-of-the-art face recognition built with deep learning.

**Database**: MongoDB is a document database, which means it stores data in JSON-like documents. We believe this is the most natural way to think about data, and is much more expressive and powerful than the traditional row/column model.

![Capture-3](https://user-images.githubusercontent.com/49821723/181609474-63277650-0210-4e74-84fa-02c722957d9d.PNG)
<p align="center">Fig 3.2 MongoDB UI</p>

**Hardware**: Surveillance system network over the entire area with cameras supporting 60 fps video streaming.

**Operating system**: Linux is a family of open-source Unix-like operating systems based on the Linux kernel, an operating system kernel 

## 4. SYSTEM FEATURES 

### 4.1 Detection and recognition

#### 4.1.1 Description and Priority 

In the system, the library ‘face_recognition’ recognizes and manipulates faces using dlib’s state-of-the-art face recognition built with deep learning. This feature involves performing detection of faces. It is a high priority function as it is the main functionality and purpose of the system to recognize the people and identify people in order to track appropriate movements.

#### 4.1.2 Stimulus/Response Sequences 

This feature involves performing detection by using the application. It is a high priority function as it is the main functionality and purpose of the system-to recognize the people and identify people in order to track appropriate movements.

#### 4.1.3 Functional Requirements

Req-1: The surveillance system should have a clean video feed streaming at approximately 60fps.
Req-2: The system hosting the processing module should be powerful enough to run deep learning models.

### 4.2 Tracking

A tracking system, also known as a locating system, is used for the observing of persons or objects on the move and supplying a timely ordered sequence of location data for further processing. In our system, tracking is achieved by parsing the log records generated.

#### 4.2.1 Description and Priority 

The purpose of the system to recognize and identify people is coupled with tracking appropriate movements. This is achieved by creating a log for each detection made from the input video stream. Below is a representation of the data structure.


For every detection made, the corresponding date-time, id of camera, id of the person (in-case of authorized users) etc are stored in a log.

#### 4.2.2 Stimulus/Response Sequences

This feature involves performing detection by using the application. It is a high priority function as it is the main functionality and purpose of the system-to recognize the people and identify people in order to track appropriate movements.



## 5. SYSTEM DESIGN


### 5.1 SYSTEM ARCHITECTURE
![Fig. 3.5.2.1 Architecture Description](https://user-images.githubusercontent.com/49821723/181614041-b928dfe5-f1c5-464e-aafb-9578e8426068.png)
<p align="center">Fig. 5.1 System Architecture</p>


The entire system is modelled into two main components: 
Backend or the intelligence component
User interface
The intelligence component of the system deals with processing of the frames and creating the log. This process is computing resource intensive and accesses required data from the database. 
The user interface is an admin portal that allows the ability to add or remove authorized users, view the logs and analytics. All the movements across the geofences can be checked upon.

### 5.2 UML DIAGRAM

#### 5.2.1 Use Case Diagram
![UML](https://user-images.githubusercontent.com/49821723/181617709-d62edff9-4256-4784-b214-e8b5c4c83da2.png)


Fig 5.2.1 UML use case diagram 

The admin has access to mainly 3 components. Each of this is responsible for an exclusive task.

**1) Add or remove authorized personnel**: Through the portal, admin could add certain people as authorized. These people can then be tracked using a set of special ids. If an area is made accessible to authorized people only, any intrusion can be detected.

**2) View logs**: This allows the admin to establish a ground for looking at the recent movements of a subject. This would be handy in order to detect erroneous movements.

**3) Track movements**: In addition to the above, movements of a specific individual can be traced using the log generated.



### 6. IMPLEMENTATION

#### 6.1 MODULES

- Facial detection and Log generation
- User Interface and geofencing
- Analytics

#### 6.1.1 Facial detection and Log generation

In the system, the library ‘face_recognition’ recognizes and manipulates faces using dlib’s state-of-the-art face recognition built with deep learning. The facial detection process is as follows:
Resize input frame of video to 1/4 size for faster face recognition processing.
Using the input frame, a 2d array of bounding boxes of human faces is created using the CNN face detector. Using a GPU, this gives faster results since the GPU can process batches of images at once. 
From the faces extracted, we compare a list of face encodings against a candidate encoding to see if they match.
If a match occurs, we get a Euclidean distance for each comparison face. The distance tells how similar the faces are.
On finding familiar faces, we extract an id corresponding to the encoding and use that for further processing.
The purpose of the system to recognize and identify people is coupled with tracking appropriate movements. This is achieved by creating a log for each detection made from the input video stream.
Once a face is detected and identified, a new entry in the log is created using additional details.
These entries in the log are created per frame per face detected. These are further used to track and generate analytics.


![Capture-2](https://user-images.githubusercontent.com/49821723/181609471-565dcfdb-1bd9-4b3c-bb7e-e10a37132305.PNG)
<p align="center"> Fig 6.1.1.1 Facial recognition in action</p>

#### Three different types of logs

![Capture-4](https://user-images.githubusercontent.com/49821723/181609475-23c1b00f-feb4-4c36-b078-115df9161a2e.PNG)
<p align="center"> Fig 6.1.1.2 Logs for all detected people</p>

![Capture-5](https://user-images.githubusercontent.com/49821723/181609478-7e74ea2e-e495-4c3d-b530-71f9b4d6d229.PNG)
<p align="center"> Fig 6.1.1.3 Latest logs for every unique person detected</p>

![Capture-6](https://user-images.githubusercontent.com/49821723/181609481-37c51ee9-b606-4947-b7d2-b272930795c0.PNG)
<p align="center"> Fig 6.1.1.4 Total visit counts</p>

#### 6.1.2 User Interface and Geofencing

The user interface is a dashboard which is accessible by the admin and has a range of options that are offered by the system. 
**Add or remove authorized personnel**: Through the portal, admin could add certain people as authorized. These people can then be tracked using a set of special ids. If an area is made accessible to authorized people only, any intrusion can be detected.
**View logs**: This allows the admin to establish a ground for looking at the recent movements of a subject. This would be handy in order to detect erroneous movements.
**Track movements**: In addition to the above, movements of a specific individual can be traced using the log generated.

![Capture-8](https://user-images.githubusercontent.com/49821723/181609485-f0bdfde3-c3ee-44af-a8b5-7cf0a9899f23.PNG)
![Capture-9](https://user-images.githubusercontent.com/49821723/181609487-1b781a04-ebe0-406a-8788-b245d6aa4160.PNG)
![Capture-11](https://user-images.githubusercontent.com/49821723/181609459-07d1c878-7b40-4b50-8993-56536ff4a769.PNG)

A geofence is a virtual perimeter for a real-world geographic area. It could be dynamically generated—as in a radius around a point location, or a geo-fence can be a predefined set of boundaries.

#### 6.1.3 Analytics 

This system can execute various analytics that are cumbersome otherwise. These include performing a real time head count, identifying common movement patterns, heat maps, generating statistics w.r.t time and location per head, detailed analysis of traffic flow etc.
