import sys
import signal
import traceback

from src.manager import Manager
from src.backend.util.logger import log

if __name__ != '__main__':
    print('This file is supposed to be ran directly, not be imported!')
    sys.exit()

debug = True

manager = Manager(debug)

# Catch process end signals so we can do our cleanup
signal.signal(signal.SIGINT, manager.stop_signal)
signal.signal(signal.SIGTERM, manager.stop_signal)

try:
    manager.start()

    # keep main thread active
    while manager.active:
        pass
except Exception as e:
    track = traceback.format_exc()
    log.error('MAIN', e)
    print(track)

    manager.stop(True)
