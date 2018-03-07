#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import csv

class WebServerHandle(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # lists all elements in the CSV
            if self.path.endswith("/list"):
                # Send response status code
                self.send_response(200)
                
                # Send headers
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                # Send message back to client
                my_file = open("list.csv", 'r')
                
                output = ""
                output += "<html><head><style>body {font-family: Helvetica, Arial; color: #333}</style></head>"
                output += "<meta http-equiv='Content-Type' content='text/html; charset=utf-8'>"
                
                output += "<body><p>"
                
                # get the universities names, line by line
                for line in my_file:
                    output += line + "<br> "
                
                output += "</html></body>"
                
                self.wfile.write(bytes(output, "utf-8"))
                return

            # If action is done successfully
            if self.path.endswith("/success"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><head><style>body {font-family: Helvetica, Arial; color: #333}</style></head>"
                output += "<body><h3>Action done!</h3>"
                output += "</html></body>"
                self.wfile.write(bytes(output, "utf-8"))
                return

            # If action is not done
            if self.path.endswith("/fail"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><head><style>body {font-family: Helvetica, Arial; color: #333}</style></head>"
                output += "<body><h3>Action failed!</h3>"
                output += "</html></body>"
                self.wfile.write(bytes(output, "utf-8"))
                return

            # Form to ADD a new university
            if self.path.endswith("/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><head><style>body {font-family: Helvetica, Arial; color: #333}</style></head>"
                output += "<body><h3>Add new University</h3>"
                output += "<form method='POST' enctype='multipart/form-data' action='/new'>"
                output += "<input name='newUniversityName' type='text' placeholder='New University Name'> "
                output += "<input type='submit' value='Add University'>"
                output += "</form></html></body>"
                self.wfile.write(bytes(output, "utf-8"))
                return

            # Form to DELETE a new university
            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><head><style>body {font-family: Helvetica, Arial; color: #333}</style></head>"
                output += "<body><h3>Delete University</h3>"
                output += "<form method='POST' enctype='multipart/form-data' action='/delete'>"
                output += "<input name='UniversityName' type='text' placeholder='University name'> "
                output += "<input type='submit' value='DELETE'>"
                output += "</form></html></body>"
                self.wfile.write(bytes(output, "utf-8"))
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            # request to ADD new University
            if self.path.endswith("/new"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    print("Fields value is", fields)
                    university_name = fields.get('newUniversityName')
                    print("University name is ", university_name[0].decode("utf-8"))
                    
                    with open('list.csv', 'a') as my_file:
                        my_file.write(university_name[0].decode("utf-8"))
                        my_file.write("\n")

                        print("University added to CSV")
                    
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/success')
                    self.end_headers()

            # request to DELETE University
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    print("Fields value is", fields)
                    university_name = fields.get('UniversityName')
                    university = university_name[0].decode("utf-8")
                    print("University to DELETE is ", university)

                    name_list = []
                    is_in_list = False

                    # Verifies if the element exists in the CSV
                    with open('list.csv', 'r') as my_file:
                        reader = csv.reader(my_file)
                        r_list = list(reader)
                        for element in r_list:
                            if (len(element)): name_list.append(str(element[0]))
                        print('BEFORE DELETION: ', name_list)

                    is_in_list = university in name_list
                    print('Is university in list? ', is_in_list)

                    if is_in_list:
                        name_list.remove(university)
                        print('DELETION SUCCEED! NEW LIST: ', name_list)
                        with open('list.csv', 'w') as f:
                            writer = csv.writer(f, delimiter='\n')
                            writer.writerow(name_list)

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    if is_in_list:
                        self.send_header('Location', '/success')
                    else:
                        self.send_header('Location', '/fail')
                    self.end_headers()
        except:
            print("Inside the exception block")


def main():
    try:
        server_address = ('', 8000)
        server = HTTPServer(server_address, WebServerHandle)
        print("Starting web server on the port 8000..")
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C entered. Shutting down the server..')
        server.socket.close()

if __name__ == '__main__':
    main()

