import http.server
import socketserver
import termcolor
import json
import http.client
from seq import Seq

# Define the Server's port
PORT = 8000


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # IN this simple server version:
        # We are NOT processing the client's request
        # It is a happy server: It always returns a message saying
        # that everything is ok

        # Message to send back to the clinet
        if self.path == '/' or self.path == '/index.html':
            filename = 'index.html'
            with open(filename, 'r') as f:
                contents = f.read()
        elif '/listSpecies' in self.path:
            try:
                if 'limit=' in self.path:
                    limit = self.path.split('limit=')[1]
                    print(limit)
                    conn = http.client.HTTPConnection('rest.ensembl.org')
                    conn.request("GET", "/info/species?content-type=application/json")
                    # -- Wait for the server's response
                    r1 = conn.getresponse()
                    # -- Print the status
                    print()
                    print("Response received: ", end='')
                    print(r1.status, r1.reason)
                    # -- Read the response's body and close
                    # -- the connection
                    text_json = r1.read().decode("utf-8")
                    resp = json.loads(text_json)
                    species_l = resp['species']
                    conn.close()
                    contents = """
                            <html>
                            <body style="background-color: D7B7BC;"><FONT FACE="monospace" SIZE = 5 COLOR = 'white'><h3>List of the chosen limited species </h3></FONT>
                            <ol>"""
                    limit = int(limit)
                    counter = 0
                    for specie in species_l:
                        contents = contents + "<li>" + specie['display_name'] + "</li>"
                        counter = counter + 1
                        if counter == limit:
                            break
                    contents = contents + """</ol>
                            </body>
                            </html>
                            """
                else:
                    conn = http.client.HTTPConnection('rest.ensembl.org')
                    conn.request("GET", "/info/species?content-type=application/json")
                    # -- Wait for the server's response
                    r1 = conn.getresponse()
                    # -- Print the status
                    print()
                    print("Response received: ", end='')
                    print(r1.status, r1.reason)
                    # -- Read the response's body and close
                    # -- the connection
                    text_json = r1.read().decode("utf-8")
                    resp = json.loads(text_json)
                    species_l = resp['species']
                    contents = """
                                            <html>
                                            <body style="background-color: D7B7BC;"><FONT FACE="monospace" SIZE = 5 COLOR = 'white'><h3>List of all the species </h3></FONT>
                                            <ol>"""

                    for specie in species_l:
                        contents = contents + "<li>" + specie['display_name'] + "</li>"

                    contents = contents + """</ol>
                                            </body>
                                            </html>
                                            """
            except ValueError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except KeyError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except TypeError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()

        elif '/karyotype' in self.path:
            try:
                specie = self.path.split('=')[1]
                conn = http.client.HTTPConnection('rest.ensembl.org')
                conn.request("GET", "/info/assembly/"+specie+"?content-type=application/json")
                r1 = conn.getresponse()
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                text_json = r1.read().decode("utf-8")
                resp = json.loads(text_json)
                karyotype_l = resp['karyotype']
                print(karyotype_l)
                contents = """
                                                        <html>
                                                        <body style="background-color: D7B7BC;"><FONT FACE="monospace" SIZE = 5 COLOR = 'white'><h3>Chromosomes of the chosen specie: </h3></FONT>
                                                        <ul>"""

                for elem in karyotype_l:
                    contents = contents + "<li>" + elem + "</li>"

                contents = contents + """</ul>
                                                        </body>
                                                        </html>
                                                        """
            except IndexError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except TypeError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except ValueError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except KeyError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()


        elif '/chromosomeLength' in self.path:
            try:
                slice = self.path.split('&')[1]
                chromo = slice.split('=')[1]
                slice2 = self.path.split('&')[0]
                specie = slice2.split('=')[1]
                print("The chromosome number to study its length is: ", chromo)
                print("The specie to study is: ", specie)
                conn = http.client.HTTPConnection('rest.ensembl.org')
                conn.request("GET", "/info/assembly/" + specie + "?content-type=application/json")
                r1 = conn.getresponse()
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                text_json = r1.read().decode("utf-8")
                resp = json.loads(text_json)
                info = resp['top_level_region']
                length = 0
                for elem in info:
                    if elem['name'] == chromo:
                        length = str(elem['length'])
                print(length)
                contents = """
                                                                    <html>
                                                                    <body style="background-color: D7B7BC;"><FONT FACE="monospace" SIZE = 5 COLOR = 'white'><h3>The length of the chromosome of the chosen specie is: </h3></FONT>
                                                                    <ul>"""


                contents = contents + "<li>" + length + "</li>"

                """</ul>
                                                                    </body>
                                                                    </html>
                                                                    """
            except ValueError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except KeyError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except TypeError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()



        elif '/geneSeq' in self.path:
            try:
                gene = self.path.split('=')[1]

                conn = http.client.HTTPConnection('rest.ensembl.org')
                conn.request("GET", "/homology/symbol/human/" + gene + "?content-type=application/json")
                r1 = conn.getresponse()
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                text_json = r1.read().decode("utf-8")
                resp = json.loads(text_json)
                id = resp['data'][0]['id']
                print(id)

                conn.request("GET", "/sequence/id/" + id + "?content-type=application/json")
                r1 = conn.getresponse()
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                text_json = r1.read().decode("utf-8")
                resp = json.loads(text_json)
                #print(resp)
                sequence = resp['seq']
                print(sequence)

                contents = """
                                                                    <html>
                                                                    <body style="background-color: D7B7BC;"><FONT FACE="monospace" SIZE = 5 COLOR = 'white'><h3>The sequence of the given human gene is: </h3></FONT>
                                                                    <ul>"""


                contents = contents + "<li>" + sequence + "</li>"

                """</ul>
                                                                    </body>
                                                                    </html>
                                                                    """
            except ValueError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except KeyError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except TypeError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()

        elif '/geneInfo' in self.path:
            try:
                gene = self.path.split('=')[1]
                conn = http.client.HTTPConnection('rest.ensembl.org')
                conn.request("GET", "/homology/symbol/human/" + gene + "?content-type=application/json")
                r1 = conn.getresponse()
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                text_json = r1.read().decode("utf-8")
                resp = json.loads(text_json)
                id = resp['data'][0]['id']
                print(id)

                conn.request("GET", "/overlap/id/" + id + "?feature=gene;content-type=application/json")
                r1 = conn.getresponse()
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                text_json = r1.read().decode("utf-8")
                resp = json.loads(text_json)

                start = resp[0]['start']
                end = resp[0]['end']
                length = end-start
                chromo_name = resp[0]['assembly_name']

                contents = """
                                                                    <html>
                                                                    <body style="background-color: D7B7BC;"><FONT FACE="monospace" SIZE = 5 COLOR = 'white'><h3>The information asked of the given human gene is: </h3></FONT>
                                                                    <ul>"""


                contents = contents + "<li>" + """<FONT FACE="monospace" SIZE = 5 COLOR = 'darkslategray'><h5>The start of the sequence is: </h5></FONT>""" + str(start) + "</li>"
                contents = contents + "<li>" + """<FONT FACE="monospace" SIZE = 5 COLOR = 'darkslategray'><h5>The end of the sequence is: </h5></FONT>""" + str(end) + "</li>"
                contents = contents + "<li>" + """<FONT FACE="monospace" SIZE = 5 COLOR = 'darkslategray'><h5>The length of the sequence is: </h5></FONT>""" + str(length) + "</li>"
                contents = contents + "<li>" + """<FONT FACE="monospace" SIZE = 5 COLOR = 'darkslategray'><h5>The name of the gene is: </h5></FONT>""" + str(chromo_name) + "</li>"

                """</ul>
                                                                    </body>
                                                                    </html>
                                                                    """
            except ValueError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except KeyError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except TypeError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()

        elif '/geneCalc' in self.path:
            try:
                gene = self.path.split('=')[1]
                conn = http.client.HTTPConnection('rest.ensembl.org')
                conn.request("GET", "/homology/symbol/human/" + gene + "?content-type=application/json")
                r1 = conn.getresponse()
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                text_json = r1.read().decode("utf-8")
                resp = json.loads(text_json)
                id = resp['data'][0]['id']
                print(id)

                conn.request("GET", "/sequence/id/" + id + "?content-type=application/json")
                r1 = conn.getresponse()
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                text_json = r1.read().decode("utf-8")
                resp = json.loads(text_json)
                # print(resp)
                sequence = resp['seq']
                print(sequence)

                s1 = Seq(sequence)
                total_length = len(sequence)

                pa = s1.perc('A')
                pt = s1.perc('T')
                pc = s1.perc('C')
                pg = s1.perc('G')

                contents = """
                                                                    <html>
                                                                    <body style="background-color: D7B7BC;"><FONT FACE="monospace" SIZE = 5 COLOR = 'white'><h3>The calculations asked of the given sequence is: </h3></FONT>
                                                                    <ul>"""


                contents = contents + "<li>" + """<FONT FACE="monospace" SIZE = 5 COLOR = 'darkslategray'><h5>The total lenght of the sequence is: </h5></FONT>""" + str(total_length) + "</li>"
                contents = contents + "<li>" + """<FONT FACE="monospace" SIZE = 5 COLOR = 'darkslategray'><h5>The percentage of A's in the sequence is: </h5></FONT>""" + str(pa) + "</li>"
                contents = contents + "<li>" + """<FONT FACE="monospace" SIZE = 5 COLOR = 'darkslategray'><h5>The percentage of T's in the sequence is: </h5></FONT>""" + str(pt) + "</li>"
                contents = contents + "<li>" + """<FONT FACE="monospace" SIZE = 5 COLOR = 'darkslategray'><h5>The percentage of C's in the sequence is: </h5></FONT>""" + str(pc) + "</li>"
                contents = contents + "<li>" + """<FONT FACE="monospace" SIZE = 5 COLOR = 'darkslategray'><h5>The percentage of G's in the sequence is: </h5></FONT>""" + str(pg) + "</li>"
                """</ul>
                                                                    </body>
                                                                    </html>
                                                                    """
            except IndexError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except ValueError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except KeyError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except TypeError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()

        elif '/geneList' in self.path:
            try:
                slice = self.path.split('&')[1]
                start = slice.split('=')[1]
                slice2 = self.path.split('&')[0]
                chromo = slice2.split('=')[1]
                slice3 = self.path.split('&')[2]
                end = slice3.split('=')[1]
                print('The number of chromosome is: ', chromo)
                print('The start point is: ', start)
                print('The end point is: ', end)
                conn = http.client.HTTPConnection('rest.ensembl.org')
                conn.request("GET", "/overlap/region/human/" + str(chromo) + ":" + str(start) + "-" + str(end) + "?content-type=application/json;feature=gene;feature=transcript;feature=cds;feature=exon")
                r1 = conn.getresponse()
                print()
                print("Response received: ", end='')
                print(r1.status, r1.reason)
                text_json = r1.read().decode("utf-8")
                resp = json.loads(text_json)
                contents = """
                                                                    <html>
                                                                    <body style="background-color: D7B7BC;"><FONT FACE="monospace" SIZE = 5 COLOR = 'white'><h3>The names of the genes located in the chromosome asked from the start to end positions are: </h3></FONT>
                                                                    <ul>"""
                for elem in resp:
                    position1 = elem['feature_type']

                    if position1 == "gene":
                        position2 = elem['id']
                        print(position2)
                        contents = contents + "<li>" + 'The name of the chromosome is: ' + str(position2) + "</li>"

                    """</ul>
                                                                            </body>
                                                                            </html>
                                                                            """
            except ValueError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except KeyError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except TypeError:
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()



        else:
            filename = 'error.html'
            with open(filename, 'r') as f:
                contents = f.read()



        # Generating the response message
        self.send_response(200)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


# ------------------------
# - Server MAIN program
# ------------------------
# -- Set the new handler
Handler = TestHandler
socketserver.TCPServer.allow_reuse_address = True

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()

print("")
print("Server Stopped")