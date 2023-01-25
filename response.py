from requestParser import ClientRequest

from os import path
import mimetypes
import http_headers as header

class Response:
    def __init__(self, request: ClientRequest):
        self.request = request
        self.dirPath = self._getPath()
        self.statusCode = self._getStatusCode()
        self.body = self._encodeBody()
        self.mime = self._getMimeType()
        self.head = self._encodeHead()

    def _getPath(self):
        if not self.request.isValid(): return None
        
        requestPath = getattr(self.request, 'path')
        #Format the path to get expected result frrom isdir
        if requestPath != '/':
            #Return 200 on root request (despite no body)
            requestPath = requestPath.lstrip('/')
        
        return requestPath

    def _isProperPath(self):
        return path.isdir(self.dirPath) and self.dirPath.endswith('/')

    def _isGet(self):
        return getattr(self.request, 'method') == 'GET'

    def _getStatusCode(self):
        #Bad Request
        if not self.request.isValid():
            return 400
        #Method Not Allowed (Must supply allow header)
        elif not self._isGet():
            return 405
        #OK
        elif self._isProperPath() or path.isfile(self.dirPath) :
            return 200
        #Moved Permanently (Must supply location header)
        elif path.isdir(self.dirPath):
            return 301
        #Not Found
        else :
            return 404

    def _getMimeType(self):
        mimetype = mimetypes.guess_type(self.dirPath)
        return mimetype

    def _encodeBody(self):
        if path.isfile(self.dirPath):
            with open(self.dirPath, 'rb') as body:
                return body.read()
        #Send index.html of requested directory if such file exists
        elif self._isProperPath():
            try:
                #Make both paths consistent
                with open(self.dirPath + 'index.html', 'rb') as body:
                    return body.read()
            except :
                return b''
        else:
            return b''

    def _encodeHead(self):
        headerSet = b''
        encode = True

        headerSet += header.getStatusHeader(self.statusCode, encode)
        headerSet += header.getDateHeader(encode)
        #if not self._isProperPath():
            #headerSet += header.getLocationHeader(self.dirPath + '/index.html', encode)
        if not self._isGet():
            headerSet += header.getAllowHeader(encode)
        if self.body:
            headerSet += header.getLengthHeader(self.body, encode)
        headerSet += header.getConnectionHeader(encode = encode)
        headerSet += header.getMimeHeader(self.mime, encode)

        return headerSet

    def encode(self):
        httpResponse = self.head + b'\r\n' + self.body
        return httpResponse

if __name__ == '__main__':
    sampleReq = b'GET / HTTP/1.1\r\nHost: 127.0.0.1:8080\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nSec-Fetch-Dest: document\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-Site: none\r\nSec-Fetch-User: ?1'
    test = ClientRequest(sampleReq)
    m = Response(test)
    a = m.encode()