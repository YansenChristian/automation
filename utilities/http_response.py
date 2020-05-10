def returnMessage(statusCode, message):
    return {
        "status": statusCode,
        "message": message
    }, statusCode


def returnData(statusCode, data):
    return {
        "status": statusCode,
        "data": data
    }, statusCode
