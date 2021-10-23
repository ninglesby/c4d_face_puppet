import c4d
import serial
import time
#Welcome to the world of Python

def set_axis():
    axis_vals = [
    op[c4d.ID_USERDATA, 2],
    op[c4d.ID_USERDATA, 3],
    op[c4d.ID_USERDATA, 4],
    op[c4d.ID_USERDATA, 5],
    op[c4d.ID_USERDATA, 6]
    ]

    index = 1
    for val in axis_vals:

        if history.get(index) != val:
            command_str = "<2,{},{},0>".format(index, val).encode("utf-8")
            ser.write(command_str)
            history[index] = val
        index+=1

def stop_axis():
    print("Stop")
    command_str = b"<6,0,0,0>"
    ser.write(command_str)



def realtime_animation(first_frame):
    fps = c4d.documents.GetActiveDocument().GetFps()
    axis_vals = [
    op[c4d.ID_USERDATA, 2],
    op[c4d.ID_USERDATA, 3],
    op[c4d.ID_USERDATA, 4],
    op[c4d.ID_USERDATA, 5],
    op[c4d.ID_USERDATA, 6]
    ]

    index = 1
    for val in axis_vals:

        if history.get(index) != val:
            speed = 0
            if not first_frame:
                speed = (val-history.get(index,0))*fps

            command_str = "<5,{},{},{}>".format(index, val, speed).encode("utf-8")
            ser.write(command_str)
            history[index] = val
        index+=1


def main():

    global ser
    global history
    global running

    try:
        history
    except NameError:
        history = {}
    try:
        running
    except NameError:
        running = False
    try:
        ser
        ser_exists = True
    except NameError:
        ser_exists = False



    first_frame = False
    stop = False
    if c4d.CheckIsRunning(c4d.CHECKISRUNNING_ANIMATIONRUNNING):
        if not running:
            first_frame = True
        running = True

    else:
        if running:
            stop = True
        running = False

    if op[c4d.ID_USERDATA, 1] == 0 and ser_exists:

        if ser.isOpen():
            ser.close()
            print("Closed Connection")
        else:
            print("Connection already closed")
    elif op[c4d.ID_USERDATA, 1] and ser_exists:
        if not ser.isOpen():
            ser.open()
            print("Reopened connection")
        else:
            if running:
                #realtime_animation(first_frame)
                set_axis()
            elif stop:
                stop_axis()
            else:
                set_axis()

    elif op[c4d.ID_USERDATA, 1]:
        ser = serial.Serial('COM3', 19200, timeout=1)
        print("Initializing Connection")
        time.sleep(2)