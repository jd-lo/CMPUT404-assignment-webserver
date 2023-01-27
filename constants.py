#Contains all relevant constants

#Path related
PATH_ROOT = 'www'
INDEX_FILE = 'index.html'

#Status codes
OK = 200
METHOD_NOT_ALLOWED = 405
PERM_REDIR = 301
BAD_REQ = 400
NOT_FOUND = 404
FORBIDDEN = 403

#As defined by RFC 9110
STATUS_MAP = {
        200: 'OK',
        301: 'Moved Permanently',   
        400: 'Bad Request',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Found',    
        500: 'Internal Server Error'
    }

#Header related
MIME_DEFAULT = 'application/octet-stream'
CHAR_SET = 'utf-8'
PROTOCOL = 'HTTP/1.1'
URL_SCHEME = 'http://'
HEADER_DELIMITER = '\r\n'
