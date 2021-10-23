import os
import sys

for path in os.environ.get("pythonpath").split(os.pathsep):
    if not path in sys.path:
        sys.path.append(path)

import c4d
from c4d import gui, plugins, bitmaps
import math
import face_server

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

if not CURRENT_DIR in sys.path:
    sys.path.append(CURRENT_DIR)




PLUGIN_ID = 1052678
OBJECT_PLUGIN_ID = 1052679
BMP_PATH = os.path.join(CURRENT_DIR, 'res')

################GUI IDS###########################
[
GRP_TABS,
GRP_STREAM_TAB,
GRP_STREAM_COL,
GRP_STREAM_PAD_C1,
GRP_STREAM_PAD_TXT1,
GRP_STREAM_PAD_TOP,
GRP_STREAM_LAYOUT,
GRP_STREAM_PAD_TXT2,
GRP_PLAYBACK_TAB,
GRP_SETTINGS_TAB,
GRP_BTN_START_STREAM,
BTN_START_STREAM,
GRP_BTN_REC_STREAM,
BTN_REC_STREAM,
FILE_REC,
GRP_FILE_REC,
BTN_FILE_REC,
LABEL_FILE_REC,
GRP_FILE_PLAYBACK,
BTN_FILE_PLAYBACK,
LABEL_FILE_PLAYBACK,
FILE_PLAYBACK,
GRP_HOSTNAME,
LABEL_HOSTNAME,
COMBO_HOSTNAME,
LABEL_PORT,
NUM_PORT,
GRP_CONTROLLER,
LNK_CONTROLLER,
BTN_ADD_CONTROLLER
] = range(1000, 1030)


def distance_calc(a, b):
    dist = math.sqrt(   abs(math.pow((a.x-b.x), 2) + 
                        math.pow((a.y-b.y), 2) + 
                        math.pow((a.z-b.z), 2))
                    )
    return dist


class Menu(gui.GeDialog):

    def __init__(self):
        self.stream_button = "Play.tif"
        self.streaming = False
        self.record_button = "Record.tif"
        self.recording = False
        self.doc = c4d.documents.GetActiveDocument()



    def CreateLayout(self):
        self.SetTitle("Face Off")



        self.GroupBegin(id=GRP_STREAM_TAB, flags=c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, cols=1, title="Streaming")# <-----------Streaming Tab
        self.GroupBegin(id=GRP_STREAM_LAYOUT, flags=c4d.BFV_FIT, cols=1, rows=4)

        self.GroupBegin(id=GRP_STREAM_PAD_TOP, flags=c4d.BFV_TOP, cols=1, rows=1)
        self.AddStaticText(id=GRP_STREAM_PAD_TXT1, flags=c4d.BFV_FIT, inith=10, name="")
        self.GroupEnd() #/GRP_STREAM_PAD_TOP

        self.GroupBegin(id=GRP_STREAM_COL, flags=c4d.BFV_FIT | c4d.BFH_FIT, cols=4)

        self.AddStaticText(id=2000, flags=c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT)

        self.GroupBegin(id=GRP_BTN_START_STREAM, flags=c4d.BFH_CENTER, cols=1)
        bc = c4d.BaseContainer()
        bc.SetString(c4d.BITMAPBUTTON_TOOLTIP, "<b>Start Webcam</b><br>Boot up the mediapipe")
        bc.SetLong(c4d.BITMAPBUTTON_FORCE_SIZE, 100)
        bc.SetBool(c4d.BITMAPBUTTON_BUTTON, True)
        self.start_stream = self.AddCustomGui(BTN_START_STREAM, c4d.CUSTOMGUI_BITMAPBUTTON, "Start Stream", c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 16, 16, bc)
        self.start_stream.SetImage(os.path.join(BMP_PATH, self.stream_button))
        self.GroupEnd() #/GRP_BTN_START_STREAM



        self.AddStaticText(id=2001, flags=c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT)

        self.GroupEnd()#/GRP_STREAM_COL

    
        self.GroupEnd() #/GRP_STREAM_LAYOUT
        self.GroupEnd() #/GRP_STREAM_TAB

        return True

    def Command(self, id, msg):

        if id == BTN_START_STREAM:

            self.toggle_stream()



        return True

    def DestroyWindow(self):
        pass


    def toggle_stream(self):

        if self.streaming:
            if self.recording:
                self.toggle_record()
            self.streaming = False
            self.stream_button = "Play.tif"
            #shutdown camera
            face_server.shutdown_cam()
        else:
            self.streaming = True
            self.stream_button = "Stop.tif"
            
            try:
                face_server.start_cam()
                #start_camera
            except Exception as e:
                self.streaming = False
                self.stream_button = "Play.tif"
                print(e)
                return False

        self.start_stream.SetImage(os.path.join(BMP_PATH, self.stream_button))
        self.LayoutChanged(GRP_STREAM_COL)
        return True

def set_pos(face_landmarks):
    doc = c4d.documents.GetActiveDocument()
    obj = doc.GetFirstObject()
    
    for landmark in face_landmarks:
        for data_point in landmark.landmark:
            x = data_point.x
            y = data_point.y
            z = data_point.z
            pos = c4d.Vector(x, y, z)
            
            if obj:
                obj.SetRelPos(pos)
                obj = obj.GetNext()


class Face(plugins.CommandData):

    dialog = None

    def Execute(self, doc):

        if not self.dialog:
            self.dialog = Menu()

        return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=PLUGIN_ID, defaultw=150, defaulth=200)

    def RestoreLayout(self, sec_ref):
        if self.dialog is None:
            self.dialog = Menu()

        return self.dialog.Restore(pluginid=PLUGIN_ID, secret=sec_ref)


class FaceObject(plugins.ObjectData):

    def __init__(self):
        pass


    def Init(self):

        return True

    def Message(self, node, type, data):
        if type==c4d.MSG_DESCRIPTION_COMMAND:

            pass
            #get commands
        return True

    def AddToExecution(self, op, list):
        list.Add(op, c4d.EXECUTIONPRIORITY_ANIMATION, 1)
        frame = face_server.get_stream()
        if frame:
            set_pos(frame)
        return True

    def Execute(self, op, doc, bt, priority, flags):

        pass # do stuff
        return True
if __name__ == "__main__":

    bmp = bitmaps.BaseBitmap()
    fn = os.path.join(BMP_PATH, "faceoff_cage.jpg")
    bmp.InitWith(fn)
    plugins.RegisterCommandPlugin(  id=PLUGIN_ID,
                                    str="Faces",
                                    info=0,
                                    help="No help for you",
                                    icon=bmp,
                                    dat=Face())
    bmp = bitmaps.BaseBitmap()
    fn = os.path.join(BMP_PATH, "faceoff_cage.jpg")
    bmp.InitWith(fn)
    plugins.RegisterObjectPlugin(   id=OBJECT_PLUGIN_ID,
                                    str="FaceObject",
                                    g=FaceObject,
                                    description="FacesObject",
                                    icon=bmp,
                                    info=c4d.OBJECT_CALL_ADDEXECUTION)