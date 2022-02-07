#main server program
import http.server
import socketserver
from pyflowchart import Flowchart
import py_compile
from urllib.parse import unquote_plus

PORT = 80

Handler = http.server.SimpleHTTPRequestHandler

class S(http.server.SimpleHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def _no_response(self):
        self.send_response(200)


    '''
    def do_GET(self):
        #logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("ok GET".encode('utf-8'))
    '''
    def do_POST(self):
        file_name='d.py'
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length).decode().lstrip('code=') # <--- Gets the data itself
        clean_data=unquote_plus(post_data)
        f = open(file_name, "w")
        with f:
            f.write(clean_data)
        '''
        try:
            py_compile.compile(file_name)
        except BaseException as e:
            self._set_response()
            self.wfile.write(('Error in code:').encode('utf-8'))
        '''
        try:
            fc = Flowchart.from_code(clean_data)
            flowcode=fc.flowchart()
            print('from FlowChart:',flowcode)
            self._set_response()
            self.wfile.write(flowcode.encode('utf-8'))
        except:
            self._no_response()


with socketserver.TCPServer(("", PORT), S) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()