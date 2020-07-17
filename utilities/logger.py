import logging
from logging.handlers import SysLogHandler


Logger = None
def getLogger():
    global Logger

    syslog = SysLogHandler(address='/var/run/syslog')
    syslog.setFormatter(
        logging.Formatter(
            '%(asctime)s %(levelname)s : %(message)s',
            datefmt='%b %d %H:%M:%S'
        )
    )

    Logger = logging.getLogger()
    Logger.setLevel(logging.INFO)
    Logger.addHandler(syslog)

    Logger.info("This is a message")
    return Logger
