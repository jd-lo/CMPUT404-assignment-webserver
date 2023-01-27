#Defines the logic involved in creating various headers

import constants as constant
from email.utils import formatdate

CHAR_SET = 'utf-8'

def __format(header: str, encode = True):
    fheader = header + '\r\n'
    if encode :
        fheader = bytearray(fheader, CHAR_SET)
    return fheader

def mk_status_header(status_code: int, encode = True):
    status_header = f'{constant.PROTOCOL} {status_code} {constant.STATUS_MAP[status_code]}'
    return __format(status_header, encode)

#See README for acknowledgement
def mk_date_header(encode = True):
    date_header = f'Date: {formatdate(timeval = None, localtime = False, usegmt = False)}'
    return __format(date_header, encode)

def mk_length_header(stream, encode = True):
    length_header = f'Content-Length: {len(stream)}'
    return __format(length_header, encode)

def mk_connection_header(option = 'close', encode = True):
    if option != 'close' and option != 'keep-alive':
        raise ValueError('option must be \"close\" or \"keep-alive\"')

    connection_header = f'Connection: {option}'
    return __format(connection_header, encode)

#Does not check validity of path
def mk_location_header(filepath, encode = True):
    location_header = f'Location: {filepath}'
    return __format(location_header, encode)

def mk_allow_header(permittedMethods = ['mk'], encode = True):
    allow_header = 'Allow: '
    for method in permittedMethods:
        allowPartial += method
        if method.index() != -1:
            allowPartial += ','
    return __format(allow_header, encode)

def mk_mime_header(mimetype, encode = True):
    mime_header = f'Content-Type: {mimetype}; charset={CHAR_SET}'
    return __format(mime_header, encode)


