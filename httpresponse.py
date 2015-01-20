from httprequest import HTTPRequest
import os.path

class HTTPResponse:

    __PATH = "www"

    __MIME = {
                "html": "text/html",
                "css": "text/css"
            }

    __CODE_MAP = {
                200: "OK",
                404: "Not Found",
                400: "Bad Request",
                500: "Internal Server Error"
            }

    __HTML_BODY = "<HTML><BODY><H2>{0}</H2></BODY></HTML>"

    #pass in HTTPRequest Object as the request
    def __init__(self, request):
        self._request = request
        self._path = None

        if request.is_valid:
            self._normalizepath()

    #Getters
    @property
    def request(self):
        return self._request

    @property
    def path(self):
        return self._path

    @property
    def path_extension(self):
        if self.path_exists:
            name, extension = os.path.splitext(self.path)
            extension = extension.replace('.','')
            return extension
        else:
            return ""

    @property
    def path_exists(self):
        if self.path != None:
            return os.path.exists(self.path)
        else:
            return False

    @property
    def response(self):

        request = self.request
        code = self.__CODE_MAP[500]

        # Default mime type
        mime = self.__MIME["html"]

        content = ""
        size = 0

        if request.is_valid and self.path_exists:
            code = 200
            with open (self.path, "r") as input_file:
                content=input_file.read().replace('\n', '')
        elif request.is_valid and not self.path_exists:
            code = 404
        elif not request.is_valid:
            code = 400
        else:
            code = 500

        if code >= 300:
            content = self.__HTML_BODY.format(self.__CODE_MAP[code])

        size = len(content)

        # Set mime to correct type if we support it
        if self.__MIME.has_key(self.path_extension):
            mime = self.__MIME[self.path_extension]

        #VERSION CODE REQUESTNAME -- MIME -- LENGTH OF OUTPUT -- BODY
        return "{0} {1} {2} \r\nContent-Type: {3}\r\nContent-Length: {4}\r\nConnection: close\r\n\r\n{5}".format(
                request.http_version,code,self.__CODE_MAP[code],
                mime,
                size,
                content)

    def _normalizepath(self):
        #setup up vars
        request = self.request
        directory = os.path.realpath(self.__PATH)
        req_file = os.path.realpath(directory + request.path)

        if os.path.commonprefix([directory,req_file]) == directory:
            #did not try to specify directory bellow our main

            #add index.html
            if request.path.endswith(os.path.sep):
                req_file = req_file + os.path.sep + "index.html"

            self._path = req_file




