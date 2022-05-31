#!/usr/bin/env python

import cgi
import shutil
import subprocess
import tempfile

from http.server import HTTPServer, SimpleHTTPRequestHandler

stltostp="/web/stltostp"

def convert(source, target):
    try:
        result = subprocess.run([stltostp, source, target],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
        if result.returncode == 0:
            return (200, None)
        else:
            return (400, result.stderr)
    except Exception as e:
        return (500, str(e))

class FileConvertHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404, "Not Found")
            return
        SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0))
        if content_len == 0:
            self.send_error(400, "Missing body")
            return

        form = cgi.FieldStorage(self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],})

        if 'file' not in form:
            self.send_error(400, "No file received")
            return

        if not form['file'].filename.endswith(".stl"):
            self.send_error(400, "STL file expected")
            return

        with tempfile.NamedTemporaryFile() as stl:
            shutil.copyfileobj(form['file'].file, stl.file)

            with tempfile.NamedTemporaryFile() as step:
                (status, error) = convert(stl.name, step.name)

                if error:
                    self.send_error(status, error)
                else:
                    filename =  ".".join(form['file'].filename.split(".")[:-1]) + ".step"
                    self.log_message(f"successfully converted {filename}")
                    self.send_response(status)
                    self.send_header("Content-type", "application/octet-stream")
                    self.send_header("Content-Disposition", f"attachment; filename=\"{filename}\"")

                    self.end_headers()
                    shutil.copyfileobj(step.file, self.wfile)

def run(server_class=HTTPServer, handler_class=FileConvertHandler):
    server_address = ("0.0.0.0", 8000)
    httpd = server_class(server_address, handler_class)
    print(f"Listening to {':'.join([str(x) for x in server_address])}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
