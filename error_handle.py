import sys
from libauth import libauth
from libnotify import libnotify

def log_read(log_file):
    with open(log_file, "r") as f:
        message = f.read()
    return message

if __name__ == "__main__":
    logmodule = sys.argv[1]
    logfile = sys.argv[2]
    log_message = logmodule + "\n" + log_read(sys.argv[2])
    auth = libauth.Auth()
    notify = libnotify.Notify.notify(auth.notify_uri(), auth.notify_token(), auth.notify_channel(), log_message)
