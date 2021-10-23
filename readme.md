# Live Puppeteering Through Cinema4D

![fish](https://user-images.githubusercontent.com/29129252/138560237-d94b52bc-94b0-4366-bd74-74f9836efa87.gif)

Felt like getting a little wild one Friday night after a long week of work. I started by trying to use mediapipe in C4D. Then I remembered for some reason I had created a little project would push out data from C4D over usb to an arduino that was hooked up to some stepper motors. I had also built a little pan tilt head in the past so slop all those things together and bam.

You need to have the python library for mediapipe and pyserial accessable from within C4D. Starting at like R22 I think C4D started ignorning the pythonpath environment variable. So this plugin will add anything from the pythonpath env variable to the sys.path. This may or may not be desirable for you.

The C4D plugin has two parts. This my not be the most logical way to do this but I was adapting some older work to get this up super fast. There is the regular "Face" dialog that just opens up a big play button. This can be used to start and stop the webcam and mediapipe process. Then there is the FaceObject which is an object so that it can get picked up in the main thread of C4D's event loop. But all it really does at the moment is grab the first 468 items in C4D and move them to the position of one of the facial landmarks being provided by mediapipe.


I am then just using c4d constraints to move the object that is then hooked up with an xpresso tag to the python tag which is what is sending data over usb. It's duct tape and paper clips but it kind of works.

- [mediapipe](https://google.github.io/mediapipe/)
- [pan tilt head](https://github.com/isaac879/Pan-Tilt-Mount)
