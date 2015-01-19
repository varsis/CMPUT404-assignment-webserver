from httprequest import HTTPRequest
import os.path

class HTTPResponse:

    __PATH = "www"

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

    def _normalizepath(self):
        #setup up vars
        request = self.request
        directory = os.path.realpath(self.__PATH)
        req_file = os.path.realpath(directory + request.path)

        if os.path.commonprefix([directory,req_file]) == directory:
            #did not try to specify directory bellow our main
            self._path = req_file


