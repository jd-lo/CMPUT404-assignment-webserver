from requestParser import ClientRequest

from os import path
import mimetypes
import http_headers as header

class Response:
    def __init__(self, request: ClientRequest):
        self.request = request
        self.dirPath = getattr(self.request, 'path') if self.request.isValid() else None 
        self.statusCode = self._getStatusCode()
        self.mime = self._getMimeType()
        self.body = self._encodeBody()
        self.head = self._encodeHead()

    def _getStatusCode(self):
        #Bad Request
        if not self.request.isValid():
            return 400
        #Method Not Allowed (Must supply allow header)
        elif getattr(self.request, 'method') != 'GET':
            return 405
        #OK
        elif path.exists(self.dirPath) or path.isfile(self.dirPath):
            return 200
        #Moved Permanently (Must supply location header)
        elif path.exists(self.dirPath + '/'):
            return 301
        #Not Found
        else :
            return 404

    def _getMimeType(self):
        mimetype = mimetypes.guess_type(self.filepath)

        if mimetype:
            return mimetype
        else :
            return 'application/octet-stream' #Most generic when none found

    def _encodeBody(self):
        with open(self.filepath, 'rb') as body:
            return body.read()

    def _encodeHead(self):
        headerSet = b''
        encode = True

        headerSet += header.getStatusHeader(self.statusCode, encode)
        headerSet += header.getDateHeader(encode)
        if self.statusCode == 301:
            headerSet += header.getLocationHeader(self.dirPath.join('/'), encode)
        if self.statusCode == 405:
            headerSet += header.getAllowHeader(encode)
        headerSet += header.getLengthHeader(self.body, encode)
        headerSet += header.getConnectionHeader(encode)
        headerSet += header.getMimeHeader(self.mime, encode)

        return headerSet

    def encode(self):
        httpResponse = self._encodeHead() + b'\r\n' + self._encodeBody()
        return httpResponse

if __name__ == '__main__':
    sampleReq = b'GET / www/ HTTP/1.1\r\nHost: 127.0.0.1:8080\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nSec-Fetch-Dest: document\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-Site: none\r\nSec-Fetch-User: ?1'
    test = ClientRequest(sampleReq)
    m = Response(test)