#Defines the logic involved in creating various headers

from email.utils import format_datetime
from itertools import always_iterable
from response import Response

#As defined by RFC 9110
STATUS_MAP = {
        200: 'OK',
        301: 'Moved Permanently',   #Supply location header
        400: 'Bad Request',
        404: 'Not Found',
        405: 'Method Not Found',    #Supply accept header
        500: 'Internal Server Error'
    }

CHAR_SET = 'utf-8'

def _format(header: str, encode = False):
    fheader = header + '\r\n'
    if encode :
        fheader = bytearray(fheader, CHAR_SET)

    return fheader

def getStatusHeader(statusCode: int, encode = False):
    protocolPartial = f'HTTP/1.1 '
    statusPartial = f'{statusCode} {STATUS_MAP[statusCode]}'

    return _format(protocolPartial + statusPartial, encode)

def getDateHeader(encode = False):
    dateHeader = f'Date: {format_datetime(timeval = None, localtime = False, usegmt = False)}'
    return _format(dateHeader, encode)

def getLengthHeader(stream, encode = False):
    lengthHeader = f'Content-Length: {len(stream)}'
    return _format(lengthHeader, encode)

def getConnectionHeader(option = 'close', encode = False):
    if option != 'close' or 'keep-alive':
        raise ValueError

    connectionHeader = f'Connection: {option}'
    return _format(connectionHeader, encode)

#Does not check validity of path
def getLocationHeader(filepath, encode = False):
    locationHeader = f'Location: {filepath}'
    return _format(locationHeader, encode)

def getAllowHeader(permittedMethods = ['GET'], encode = False):
    allowHeader = 'Allow: '
    for method in permittedMethods:
        allowPartial += method
        if method.index() != -1:
            allowPartial += ','
    return _format(allowHeader, encode)

def getMimeHeader(mimetype, encode = False):
    mimeHeader = f'Content-Type: {mimetype}; charset={CHAR_SET}'
    return _format(mimeHeader, encode)

def getAllHeaders(response: Response, encode = False):


