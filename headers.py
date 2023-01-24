#Defines the logic involved in creating various headers

from email.utils import format_datetime

#As defined by RFC 9110
statusMap = {
        200: 'OK',
        301: 'Moved Permanently',   #Supply location header
        400: 'Bad Request',
        404: 'Not Found',
        405: 'Method Not Found',    #Supply accept header
        500: 'Internal Server Error'
    }

def _format(header: str, encode = False):
    encodeMethod = 'utf-8'
    fheader = header + '\r\n'
    if encode :
        fheader = bytearray(fheader, encodeMethod)

    return fheader

def getStatusHeader(statusCode: int, encode = False):
    protocolPartial = f'HTTP/1.1 '
    statusPartial = f'{statusCode} {statusMap[statusCode]}'

    return _format(protocolPartial + statusPartial, encode)

def getDateHeader(encode = False):
    return _format(f'Date: {format_datetime(timeval = None, localtime = False, usegmt = False)}', encode)

def getContentLengthHeader(stream, encode = False):
    return _format(f'Content-Length: {len(stream)}', encode)

def getConnectionHeader(option = 'close', encode = False):
    if option != 'close' or 'keep-alive':
        raise ValueError

    return _format(f'Connection: {option}', encode)
    
def getLocationHeader(filepath, encode = False):
    pass
