class HTTPRequest:
    def __init__(self, rawText):
        self._raw = rawText;
        self._status_code = 200
        self._request_type = None
        self._path = None
        self._http_version = None
        self._headers = {}
        self._is_valid = False
        self._parse()

    #Getters
    @property
    def raw(self):
        return self._raw

    @property
    def headers(self):
        return self._headers

    @property
    def request_type(self):
        return self._request_type

    @property
    def path(self):
        return self._path

    @property
    def http_version(self):
        return self._http_version

    @property
    def is_valid(self):
        return self._is_valid

    def _parse(self):
        raw = self.raw
        # check if we have a empty line
        if raw.endswith("\r\n\r\n"):

            #strip extra empty lines
            raw = raw.strip()

            #split string on carriage returns
            lines = str.split(raw,"\r\n");

            #take the first line and see if it "valid"
            request = lines[0]
            request = str.split(request, " ")

            # Should be GET PATH HTTPVERSION
            if len(request) == 3:
                self._request_type = request[0]
                self._path = request[1]
                self._http_version = request[2]

                #remove request line
                #lines now contains only the headers
                lines.pop(0)
                headerError = self._mapHeaders(lines)

                if not headerError:
                    self._is_valid = self._validate_data()


    def _validate_data(self):
        if self.http_version == "HTTP/1.1":
            return self._validate_1_1()
        elif self.http_version == "HTTP/1.0":
            return self._validate_1_0()
        else:
            return False;

    def _validate_1_1(self):
        if self.http_version == "HTTP/1.1" and self.headers.has_key("Host"):
            return True


    def _validate_1_0(self):
        if self.http_version == "HTTP/1.0":
            return True


    def _mapHeaders(self,headers):
        self.raw_headers = headers;
        for header in headers:
            headerParts = str.split(header,":",1)
            if not self._mapHeader(headerParts):
                return False



    def _mapHeader(self,headerParts):
        # check header is formated correctly
        if len(headerParts) == 2:

            #we have keys and values(if comma seperated or duplicate values)
            key = headerParts[0]
            values = str.split(headerParts[1],',')

            #check that key doesn't exist already
            if self.headers.has_key(key):
                #if key exists, we need to combine two arrays
                self._headers[key].extend(values)
            else:
                #other wise we can just set the value
                self._headers[key] = values
            return True
        else:
            return False
