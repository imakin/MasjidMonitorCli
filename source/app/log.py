import os
import sys
import logging
import logging.handlers
from datetime import datetime
import time


basedir = os.path.dirname(os.path.realpath(sys.argv[0]) )
logdir = f"{basedir}/log"

if not os.path.exists(logdir):
    os.mkdir(logdir)

class CustomRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, maxBytes=0):
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc)
        self.maxBytes = maxBytes

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.
        """
        if self.stream is None:  # delay was set...
            self.stream = self._open()
        if self.maxBytes > 0:  # are we rolling over?
            self.stream.seek(0, os.SEEK_END)
            if self.stream.tell() >= self.maxBytes:
                return 1
        return super().shouldRollover(record)

    def doRollover(self):
        """
        Do a rollover, as described in __init__().
        """
        if self.stream:
            self.stream.close()
            self.stream = None

        # Get the current time and compute the next rollover time
        current_time = int(time.time())
        new_rollover_at = self.computeRollover(current_time)

        # Truncate the log file
        with open(self.baseFilename, 'w'):
            pass

        # Update the rollover time
        self.rolloverAt = new_rollover_at

        # Perform the base class rollover
        super().doRollover()


# Example usage
FORMAT = '%(asctime)s %(message)s'
log = logging.getLogger("MasjidMonitor")
log.setLevel(logging.DEBUG)

# Use the custom handler
handler = CustomRotatingFileHandler(f"{logdir}/log_limit.txt", when="midnight", interval=1, backupCount=10, maxBytes=100000)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter(FORMAT))
log.addHandler(handler)

# Example logging
log.info("\n\n________________________________________")
log.info("started now {}".format(datetime.now()) )

class LogOnce():
    def __init__(self):
        self.last_log = ""

    def log(self, txt):
        if self.last_log != txt:
            log.info(txt)
            self.last_log = txt

lonce = LogOnce()

def log_once(txt):
    lonce.log(txt)