from os import path

#Class of parsed fields from the byte request
#Contains method to return the appropriate response, complete with header and body.

class ClientRequest:
    def __init__(self, request: bytearray):

        self.valid = False
        parsedRequest = self._parseReqBytes(request)
        if parsedRequest:
            self.valid = True
            for field, value in parsedRequest.items():
                self.__setattr__(field, value)

    #Converts a request byte sequence into a dictionary, return None if request is not correct format.
    def _parseReqBytes(self, request: bytearray) :
        tokenStream = request.decode('utf-8')
        keyValPairs = tokenStream.split('\r\n')

        dictRequest = {}

        try:
            #The first entry "[REQ] / ... does not follow conventional pattern; deal with seperately"
            requestProtocolStr = keyValPairs.pop(0)
            sepEntries = requestProtocolStr.split(" ")
            dictRequest.update({"method": sepEntries[0], "path": sepEntries[1].lstrip('/'), "protocol": sepEntries[2]})
            
            #The next entry, Host needs to be split into respective host and port
            hostPortStr = keyValPairs.pop(0)
            sepEntries = hostPortStr.split(":")
            dictRequest.update({"host": sepEntries[1].strip(), "port": sepEntries[2]})

            #All remaining entries standard.
            for keyValStr in keyValPairs:
                keyVal = keyValStr.split(':', maxsplit = 1)
                dictRequest.update({keyVal[0].strip().lower(): keyVal[1].strip()})

            return dictRequest
        except:
            return None

    def isValid(self):
        return self.valid

    def getResponse(self):
        #Status, MIME types, body
        if not self.isValid():
            #Code 400 (Bad Request)
            pass
        elif self.getattr(self, 'method') != 'GET':
            #Code 405 (Method not allowed)
            pass
        elif self.getattr(self, 'path') != path.exists():
            #Code 301 (Redirect, provided corrected path exists)
            #Code 404 If above fails (Not found otherwise)
            pass
        elif self.getattr(self, 'path') != path.isfile():
            #Code 404 (Not found)
            pass
        else:
            #Code 200 (OK)
            pass

#For use debugging
if __name__=='__main__':
    sampleReq = b'Hello World'
    test = ClientRequest(sampleReq)