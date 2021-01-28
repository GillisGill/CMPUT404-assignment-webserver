#  coding: utf-8 
import socketserver
import os.path
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
        #print(stringGET)
        #print("\n")
        #print(stringGET)
        index_cut = stringGET.find("HTTP/") 
        index_start = stringGET.find("/") - 1
        #print("start:",index_start,"end:",index_cut,"\n")
        string_check = stringGET[index_start:index_cut:1]
        
        string_file1 = string_check.strip()
        file_name = string_file1[1::]
        #print("THIS IS STRING FILE"+string_file)
        
        
        #print("this is string_file"+string_file+"nospace")
        #print("this is string check"+string_check)
        
        i = -1
        for files in os.walk("."):
            x = str(files)
            index = x.find(file_name)
            if index > -1:
                i = index
            #print(files)
            #print(index)
        #print("INDEX IS HERE:", i)

        
        """
        if i > -1:
            if string_check.find("/base.css") > 0:
                print("in css")
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n",'utf-8'))
            elif string_check.find("/index.html") > 0:
                print("in html")
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n",'utf-8'))
            elif string_check.find("/") > 0:
                print("In root test")
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n",'utf-8'))
        elif i == -1:
            print("IN 404")
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
        """
        if i > -1:
            if string_check.find(".css") > -1:
                print("in css")
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n",'utf-8'))
            elif string_check.find(".html") > -1:
                print("in html")
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n",'utf-8'))
            else:
                print("in root")
                self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n",'utf-8'))
        else:
            print("in 404")
            self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n",'utf-8'))
            #self.request.sendall(bytearray("HTTP/1.1 200 OK\r\n",'utf-8'))


            
        


       

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
