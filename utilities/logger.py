import logging
from logging.handlers import SysLogHandler


Logger = None
def getLogger():
    global Logger

    syslog = SysLogHandler(address=('logs6.papertrailapp.com', 33527))
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
