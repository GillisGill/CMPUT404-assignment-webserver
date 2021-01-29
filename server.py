#  coding: utf-8 
import socketserver
import os.path
# Copyright 2020 Abram Hindle, Eddie Antonio Santos, Navjit Gill
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        
        stringGET = str(self.data)

        # Find indexes in request
        index_cut = stringGET.find("HTTP/") 
        index_start = stringGET.find("/") - 1

        # Check for illegal method
        index_method = stringGET.find(" ")
        string_method = stringGET[0:index_method:1]
        if string_method.find("PUT") != -1:
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))
        elif string_method.find("POST") != -1:
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))
        elif string_method.find("DELETE") != -1:
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))

        # Index String
        string_check = stringGET[index_start:index_cut:1]
        string_file1 = string_check.strip()
        file_name = string_file1[1::]

        last_index = len(file_name) - 1

        # Check for / at the end
        if last_index > 0 and file_name[last_index] == "/":
            file_name = file_name[0:last_index]

        
        # append www to path
        if file_name == "":
            file_name = "./www"+file_name
        else:
            file_name = "./www/"+file_name

        # split into path and file and fix
        path_files = file_name.rsplit('/', 1)
        if path_files[0] == "./www":
            path_files[0] = "./www'"
        if path_files[1] != "":
            path_files[1] = "'"+path_files[1]+"'"

        # Check if file exists in provided path
        i = -1
        for files in os.walk("."):
            x = str(files)
            index_list = []
            for pathfile in path_files:
                index_app = x.find(pathfile)
                index_list.append(index_app)
            if -1 not in index_list:
                i = 1

        # If file exists in ./www apply appropriate mime-type, else 404 not found
        if i > -1:
            if string_check.find(".css") > -1:
                the_file = open(file_name,'r')
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n" + the_file.read(),'utf-8'))
                the_file.close()

            elif string_check.find(".html") > -1:
                the_file = open(file_name,'r')
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n" + the_file.read(),'utf-8'))
                the_file.close()

            elif string_check.find(".") == -1:
                slash_index = len(string_check) - 2 #account for space
                # Redirect for that of /
                if string_check[slash_index] != "/":
                    append_url = string_check.strip()
                    location_string = "http://127.0.0.1:8080"+append_url+"/"
                    self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\nLocation: "+location_string+"\r\nContent-Type: text/html\r\n",'utf-8'))

                else:
                    to_open = file_name+"/index.html"
                    the_file = open(to_open,'r')
                    self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n" + the_file.read(),'utf-8'))
                    the_file.close()

        else:
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))


       

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
