def returnMessage(statusCode, message):
    return {
        "status": statusCode,
        "message": message
    }

def returnData(statusCode, data):
    return {
        "status": statusCode,
        "data": data
    }