from requestParser import ParsedRequest
import constants as constant
from os import path as pathfinder
import mimetypes
import http_headers as header

class Response:
    def __init__(self, request: ParsedRequest):
        self.request = request
        #localhost:8080/deep -> www/deep
        self.path = constant.PATH_ROOT + request.get_field('path')
        self.status_code = self.__get_status_code()
        self.mime = self.__get_mimetype()

        #Important to get length for header
        self.body = self.__encode_body()

    def __is_proper_dir(self):
        #Checks to see if the directory follows the expected convention
        return pathfinder.isdir(self.path) and self.path.endswith('/')

    def __dir_has_index(self):
        return pathfinder.exists(self.path + constant.INDEX_FILE)

    def __method_is_get(self):
        return self.request.get_field('method') == 'GET'

    #TODO constant.FORBIDDEN if request for a resource above www 
    def __get_status_code(self):
        if not self.request.is_valid():
            return constant.BAD_REQ
        elif not self.__method_is_get():
            return constant.METHOD_NOT_ALLOWED
        #If directory is not as expected, indicate a redirection to corrected path
        elif pathfinder.isdir(self.path) and not self.__is_proper_dir():
            return constant.PERM_REDIR
        #If index.html is not in the directory, we have nothing to display!
        elif pathfinder.isdir(self.path) and self.__dir_has_index() or pathfinder.isfile(self.path):
            return constant.OK
        else:
            return constant.NOT_FOUND
    
    def __get_mimetype(self):
        #Not unpacking tuple will result in unit test fail :(
        if pathfinder.isfile(self.path):
            (mimetype, value) = mimetypes.guess_type(self.path)
        elif self.__dir_has_index():
            (mimetype, value) = mimetypes.guess_type(self.path + constant.INDEX_FILE)
        else:
            mimetype = constant.MIME_DEFAULT

        return mimetype

    #Helper for wrapping headers in the proper byte-encoded format
    def __encode_head(self):
        #Append encoded headers as required
        headers = b''

        headers += header.mk_status_header(self.status_code)
        headers += header.mk_date_header()
        headers += header.mk_connection_header()
        headers += header.mk_mime_header(self.mime)
        headers += header.mk_length_header(self.body)
        #Only for methods no permitted
        if not self.__method_is_get():
            headers += header.mk_allow_header()
        #Only for redirects
        if not self.__is_proper_dir() and not pathfinder.isfile(self.path):
            #Redirect to /path instead of www/path (www is only for internal server usage)
            redirect_URL = f'{constant.URL_SCHEME}{self.request.get_field("host")}{self.request.get_field("path")}/'
            headers += header.mk_location_header(redirect_URL)

        return headers

    #Helper for wrapping the body in the proper byte-encoded format
    def __encode_body(self):
        try:
            if pathfinder.isfile(self.path):
                with open(self.path, 'rb') as body:
                    return body.read()
            #Guaranteed to be correct directory pathing (ends with /) since 301 redirects, but redundant to be super safe.
            elif self.__is_proper_dir() and self.__dir_has_index():
                with open(f'{self.path}{constant.INDEX_FILE}', 'rb') as body:
                    return body.read()
            else:
                return b''
        except:
            return b''

    def encode(self):
        return self.__encode_head() + constant.HEADER_DELIMITER.encode(constant.CHAR_SET) + self.body

if __name__ == '__main__':
    sampleReq = b'GET / HTTP/1.1\r\nHost: 127.0.0.1:8080\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nSec-Fetch-Dest: document\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-Site: none\r\nSec-Fetch-User: ?1'
    test = ParsedRequest(sampleReq)
    m = Response(test)
    a = m.encode()