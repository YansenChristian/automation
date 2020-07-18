import logging
import os
import socket
from logging.handlers import SysLogHandler
from inspect import getframeinfo, stack


EGRESS_LOG_MESSAGE_FORMAT = "[Egress] URL: {url:s} | Method: {method:s} | Status: {status_code:d} | Request Header: {request_header:s} | Request Body: {request_body:s} | Response Header: {response_header:s} | Response Body: {response_body:s}"
INFO_LOG_FORMAT = "{message:s}"
ERROR_LOG_FORMAT = "{message:s}, caused by {error_type:s}: {error_message:s} | File: {file_path:s} | Function: {function_name:s} | Line: {line_no:d}"
WARNING_LOG_FORMAT = "{message:s}"


class ContextFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = ContextFilter.hostname
        return True


class Log:
    Logger = None

    def __init__(self):
        syslog = SysLogHandler(address=(os.getenv("PAPERTRAIL_HOST"), int(os.getenv("PAPERTRAIL_PORT"))))
        syslog.addFilter(ContextFilter())
        syslog.setFormatter(logging.Formatter(
            '%(asctime)s %(hostname)s ' + os.getenv(
                "APP_NAME") + ' [%(levelname)s]: %(message)s',
            datefmt='%b %d %H:%M:%S'
        ))

        self.Logger = logging.getLogger()
        self.Logger.addHandler(syslog)
        self.Logger.setLevel(logging.INFO)

    def info(self, message):
        self.Logger.info(
            INFO_LOG_FORMAT.format(message=message)
        )

    def warning(self, message):
        self.Logger.warning(
            WARNING_LOG_FORMAT.format(message=message)
        )

    def error(self, message, exception):
        caller = getframeinfo(stack()[1][0])
        self.Logger.error(ERROR_LOG_FORMAT.format(
            message=message,
            error_type=type(exception).__name__,
            error_message=str(exception),
            file_path=caller.filename,
            function_name=caller.function,
            line_no=caller.lineno)
        )

    def egress(self, url, method, statusCode, requestHeader, requestBody, responseHeader, responseBody):
        truncatedRequestHeader = (requestHeader[:100] + '..') if len(requestHeader) > 100 else requestHeader
        truncatedResponseHeader = (responseHeader[:100] + '..') if len(responseHeader) > 100 else responseHeader
        truncatedRequestBody = (requestBody[:100] + '..') if len(requestBody) > 100 else requestBody
        truncatedResponseBody = (responseBody[:100] + '..') if len(responseBody) > 100 else responseBody
        self.Logger.info(EGRESS_LOG_MESSAGE_FORMAT.format(
            url=url,
            method=method,
            status_code=statusCode,
            request_header=truncatedRequestHeader,
            request_body=truncatedRequestBody,
            response_header=truncatedResponseHeader,
            response_body=truncatedResponseBody
        ))


LoggerInstance = None
def getLogger():
    global LoggerInstance
    if LoggerInstance is None:
        LoggerInstance = Log()
    return LoggerInstance

