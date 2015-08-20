import os

def set_screen_available(status):
    if status:
        if os.path.isfile('block_slide_show'):
            os.remove('block_slide_show')
    else:
        open('block_slide_show','w+').close()

def screen_available():
    if os.path.isfile('block_slide_show'):
        return False
    else:
        return True

print screen_available()

set_screen_available(True)

print screen_available()

set_screen_available(False)

print screen_available()