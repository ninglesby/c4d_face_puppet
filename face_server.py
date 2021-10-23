import cv2
import queue as Queue
import threading
import time
import mediapipe as mp

#mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

face_threads = []


class FaceServer(threading.Thread): 
    def __init__(self, queue):
        self.stop = False
        self.queue = queue

        face_threads.append(self)
        threading.Thread.__init__(self)



    def run(self):

        # For webcam input:
        print("webcam started")
        cap = cv2.VideoCapture(0)
        with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
            
            start_time = time.time()    
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                      print("Ignoring empty camera frame.")
                      # If loading a video, use 'break' instead of 'continue'.
                      continue
        
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(image)
        
                # Draw the face mesh annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_face_landmarks:
                    try:
                        self.queue.get_nowait() # clean queue data
                    except Queue.Empty:
                        pass
                    self.queue.put(results.multi_face_landmarks) # put data
                
                if self.stop:
                    break
            cap.release()

    def close(self):
        self.stop = True


class StreamQueue(threading.Thread): # when there's data, get data

    def __init__(self, queue, obj=None):
        self.stop = False
        self.queue = queue
        face_threads.append(self)
        self.obj = obj
        self.frame = None
        threading.Thread.__init__(self)
        self.counter = 0
        self.timer = time.time()
        self.fps_counter = False

    def run(self):

        while self.stop != True:
            
            try:
                data = self.queue.get(timeout=2)
                self.frame = data
                if self.fps_counter:
                    delta = time.time() - self.timer 
                    if  time.time() - self.timer > 1.0:
                        print(float(self.counter)/delta)
                        self.counter = 0
                        self.timer = time.time()
                    else:
                        self.counter += 1

            except Queue.Empty:
                pass


    def close(self):
        self.stop = True

def shutdown_cam():
    global face_threads

    for s in face_threads:
        s.close()
    face_threads = []
    print("shutdown")

def start_cam():
    q = Queue.Queue(maxsize=1)

    f = FaceServer(q)
    s = StreamQueue(q)
    f.start()
    s.start()

     
def get_stream():

    try:
        for thread in face_threads:
            if type(thread).__name__ == 'StreamQueue':

                return thread.frame
    except NameError:
        return None