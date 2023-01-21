#Takes a request in its byte form and returns a dictionary of its
#expected key-value pairs.

def parseReqBytes(byteStream: bytearray) :

    tokenStream = byteStream.decode('utf-8')
    keyValPairs = tokenStream.split('\r\n')

    dictRequest = {}

    #The first entry "[REQ] / ... does not follow conventional pattern; deal with seperately"
    requestProtocolStr = keyValPairs.pop(0)
    sepEntries = requestProtocolStr.split(" ")
    dictRequest.update({"Method": sepEntries[0], "Path": sepEntries[1], "Protocol": sepEntries[2]})
    
    #The next entry, Host needs to be split into respective host and port
    hostPortStr = keyValPairs.pop(0)
    sepEntries = hostPortStr.split(":")
    dictRequest.update({"Host": sepEntries[1].strip(), "Port": sepEntries[2]})

    #All remaining entries standard.
    for keyValStr in keyValPairs:
        keyVal = keyValStr.split(':', maxsplit = 1)
        dictRequest.update({keyVal[0].strip(): keyVal[1].strip()})

    return dictRequest


sampleReq = b'GET / HTTP/1.1\r\nHost: 127.0.0.1:8080\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nSec-Fetch-Dest: document\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-Site: none\r\nSec-Fetch-User: ?1'
sampleReq2 = b'GET /favicon.ico HTTP/1.1\r\nHost: 127.0.0.1:8080\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0\r\nAccept: image/avif,image/webp,*/*\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nReferer: http://127.0.0.1:8080/\r\nSec-Fetch-Dest: image\r\nSec-Fetch-Mode: no-cors\r\nSec-Fetch-Site: same-origin'
sampleReq3 = b'Hello World' #When we pipe in something using netcat...
sampleReq4 = b'GET / HTTP/1.1\r\nHost: 127.0.0.1:8080\r\nUser-Agent: curl/7.68.0\r\nAccept: */*'

myDict = parseReqBytes(sampleReq4)
    