import constants as constant


class ParsedRequest:
    def __init__(self, request: bytearray):

        self.valid = False
        self.header_dict = {}

        try:
            self.__parse_headers(request)
            if self.header_dict:
                self.valid = True
                for field, value in self.header_dict.items():
                    self.__setattr__(field, value)
        except Exception as e:
            print(e)
        
    #Mutates dictionary of headers to contain all relevant fields for easy access
    def __parse_headers(self, request: bytearray) :
        tokenStream = request.decode(constant.CHAR_SET)
        headers = tokenStream.split(constant.HEADER_DELIMITER)

        try:
            #The first entry "[REQ] / ... does not follow conventional pattern; deal with seperately"
            self.__parse_initial_header(headers.pop(0))
            
            #All remaining entries standard. (Some additional handling for host)
            [self.__parse_std_header(header) for header in headers]
            #self.__split_host_port()

        except Exception as e:
            print('Bad Request', e)

    def __parse_initial_header(self, header: str):
        sep_entries = header.split(' ')
        #Per HTTP specifications
        self.header_dict.update({'method': sep_entries[0], 'path': sep_entries[1], 'protocol': sep_entries[2]})

    def __parse_std_header(self, header: str):
        #Limit 1 due to issue parsing host/port header
        sep_entries = header.split(':', maxsplit = 1)

        field = sep_entries[0].strip().lower()
        value = sep_entries[1].strip()

        self.header_dict.update({field:value})
    
    def __split_host_port(self):
        header = self.header_dict['host']

        sep_entries = header.split(':')

        self.header_dict.update({'host': sep_entries[0]})
        self.header_dict.update({'port': sep_entries[1]})

    def is_valid(self):
        return self.valid

    def get_field(self, field_name: str):
        field_name = field_name.lower()
        if field_name in self.header_dict:
            return self.header_dict[field_name]
        else:
            return None

if __name__ == "__main__":
    #For use debugging
    req = b'bananas GET / HTTP/1.1\r\nAccept-Encoding: identity\r\nHost: 127.0.0.1:8080\r\nUser-Agent: Python-urllib/3.8\r\nConnection: close'
    req2 = b'GET /www/ HTTP/1.1\r\nHost: 127.0.0.1:8080\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nSec-Fetch-Dest: document\r\nSec-Fetch-Mode: navigate\r\nSec-Fetch-Site: none\r\nSec-Fetch-User: ?1'
    a = ParsedRequest(req2)
    print(a.get_field("host"))