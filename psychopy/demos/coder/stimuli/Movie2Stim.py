"""
Demo using the experimental movie2 stim to play a video file. Path of video
needs to updated to point to a video you have. movie2 does /not/ require
avbin to be installed.

Movie2 does require:
~~~~~~~~~~~~~~~~~~~~~

1. Python OpenCV package (so openCV libs and the cv2 python interface).
For Windows, a binary installer is available at http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv
For Linux, it is available via whatever package manager you use.
For OSX, ..... ?
2. VLC application. Just install the standard VLC (32bit) for your OS. http://www.videolan.org/vlc/index.html

To play a video, you /must/:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

a. Create a visual.MovieStim2(..) instance; pretend it is called mov.
b. Call mov.play() when you want to start playing the video.
c. Call win.flip(), which will display the first frame of the video.
d. In the experiment loop, call mov.draw() followed by win.flip() to draw
   the video frame again mov.draw() determines if the current frame,
   or the next frame should be redrawn and does so accordingly. If the next
   frame is drawn, mov.draw() will return the frame index just drawn. If
   the same frame is drawn as before, None is returned.

This method call sequence must be followed. This should be improved (I think)
depending on how movie stim calls are actually made. The current movie stim
code doc's seem a bit mixed in message.

Current known issues:
~~~~~~~~~~~~~~~~~~~~~~

1. Loop functionality are known to be broken at this time.
2. Auto draw not implemented.
3. Video must have 3 color channels.
4. Intentional Frame dropping (to keep video playing at expected rate on slow machines) is not yet implemented.

What does work so far:
~~~~~~~~~~~~~~~~~~~~~~~~~

1. mov.setMovie(filename) / mov.loadMovie(filename)
2. mov.play()
3. mov.pause()
4. mov.seek()
4. mov.stop()
5. mov.set/getVolume()
6. Standard BaseVisualStim, ContainerMixin methods, unless noted above.

Testing has only been done on Windows and Linux so far.
"""

from psychopy import visual, core, event
import time

videopath=r'D:\Dropbox\WinPython-32bit-2.7.6.0\my-code\pycvlcmovie\Epic.mp4'

win = visual.Window([1024, 768])

# Create your movie stim.
mov = visual.MovieStim2(win, videopath,
                       size=1024,
                       # pos specifies the /center/ of the movie stim location
                       pos=[0, 100],
                       flipVert=False,
                       flipHoriz=False,
                       loop=True)

keystext = "PRESS 'q' or 'escape' to Quit.\n"
keystext += "#     's': Stop/restart Movie.\n"
keystext += "#     'p': Pause/Unpause Movie.\n"
keystext += "#     '>': Seek Forward 1 Second.\n"
keystext += "#     '<': Seek Backward 1 Second.\n"
keystext += "#     '-': Decrease Movie Volume.\n"
keystext += "#     '+': Increase Movie Volume."
text = visual.TextBox(win,keystext, font_name=None, bold=False, italic=False,
                      font_size=21, font_color=[-1, -1, -1, 1],
                      textgrid_shape=(36, 7), pos=(0, -350), units = 'pix',
                      grid_vert_justification='center',
                      grid_horz_justification='left', align_horz='center',
                      align_vert='bottom',
                      autoLog=False, interpolate=True)
text.draw()

# Start the movie stim by preparing it to play and then calling flip()
mov.play()
win.flip()

while mov.status != visual.FINISHED:
    # if only a movie stim is being shown on the window, only flip when a new
    # frame should be displayed. On a 60 Hz monitor playing a 30 Hz video, this
    # cuts CPU usage of the psychopy app. by almost 50%.
    shouldflip = mov.draw()
    if shouldflip:
        text.draw()
        ftime=win.flip()
    else:
        time.sleep(0.001)

    for key in event.getKeys():
        if key in ['escape', 'q']:
            win.close()
            core.quit()
        elif key in ['s',]:
            if mov.status in [visual.PLAYING, visual.PAUSED]:
                # Stop playing the movie stim. This also unloads the current
                # movie resources, freeing the memory used. If you want to
                # play a moview again with the current mov instance, call
                # the three methods as shown in the following else statement.
                mov.stop()
                text.draw()
                win.flip()
            else:
                # If the mov has been stopped; to start it again, you must
                # load the movie file, call play, and then flip() to show the
                # first video frame.
                mov.loadMovie(videopath)
                mov.play()
                text.draw()
                win.flip()
        elif key in ['p',]:
            # If you want to pause the movie while it is playing, and then want
            # to later resume playing from where the mov was paused, do this..
            if mov.status == visual.PLAYING:
                mov.pause()
            elif mov.status == visual.PAUSED:
                mov.play()
                text.draw()
                win.flip()
        elif key == 'period':
            ntime = mov.getCurrentFrameTime()+1.0
            if ntime >= mov.duration:
                ntime = mov.duration
            mov.seek(ntime)
        elif key == 'comma':
            ntime = mov.getCurrentFrameTime()-1.0
            if ntime < 0.0:
                ntime = 0.0
            mov.seek(ntime)
        elif key == 'minus':
            cv = mov.getVolume()
            cv -= 5
            if cv < 0:
                cv = 0
            mov.setVolume(cv)
        elif key == 'equal':
            cv = mov.getVolume()
            cv += 5
            if cv > 100:
                cv = 100
            mov.setVolume(cv)
            print 'Volume:', mov.getVolume()
        else:
            print key
            #TODO: Add video seeking key shortcuts when seeking works.
            pass
core.quit()