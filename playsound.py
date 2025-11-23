import threading
import os
import sys


class Playsound(threading.Thread):

    def __init__(self, alternate = False):
        threading.Thread.__init__(self)
        self.alternate = alternate #which sound

    def run(self):
        if self.alternate:
            file = 'sounds/blip1.wav'
        else:
            file = 'sounds/s1.wav'

        try:
            if sys.platform == 'win32':
                # Windows
                import winsound
                winsound.PlaySound(file, winsound.SND_FILENAME)
            elif sys.platform == 'darwin':
                # macOS
                os.system(f'afplay {file}')
            else:
                # Linux
                # Try common Linux audio players
                if os.system(f'aplay {file} 2>/dev/null') != 0:
                    if os.system(f'paplay {file} 2>/dev/null') != 0:
                        os.system(f'ffplay -nodisp -autoexit {file} 2>/dev/null')
        except:
            return


