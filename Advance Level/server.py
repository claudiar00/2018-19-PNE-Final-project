import http.server
import socketserver
import termcolor
import http.client
import json
from seq import Seq

# Define the Server's port
PORT = 8000


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

#This is the main function of my program, that will separate the arguments of the paths in order to make it easier for whats coming after

    def main (self, path):
        dictionary = dict()
        try:
            if '?' in path:
                arguments = self.path.split('?')[1]
                arguments = arguments.split(' ')[0]
                slice = arguments.split('&')
                for elem in slice:
                    key = elem.split('=')[0]
                    value = elem.split('=')[1]
                    dictionary[key] = value
            return dictionary
        except Exception:
            pass





    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""
        json_response = False
        answer_value = 200
        # Print the request line
        termcolor.cprint(self.requestline, 'green')

        # IN this simple server version:
        # We are NOT processing the client's request
        # It is a happy server: It always returns a message saying
        # that everything is ok

        # Message to send back to the client

        #The main programming code appears below, and it starts with the index page (principal page)
        if self.path == '/' or self.path == '/index.html':
            json_response = False
            filename = 'index.html'
            with open(filename, 'r') as f:
                contents = f.read()
        #we program now the code for the path list species
        elif '/listSpecies' in self.path:
            try:
                arguments = self.main(self.path)
                if 'limit' in arguments:
                    try:
                        limit = int(arguments['limit'])
                    except Exception:
                        limit = 0
                else:
                    limit = 0


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
                if type(limit) != int:
                    answer_value = 400
                    filename = 'error.html'
                    with open(filename, 'r') as f:
                        contents = f.read()
                elif limit == 0:
                    limit = len(species_l)
                conn.close()
                #As this is the advance level of the practice the user can choose to select the json option, so if json is in arguments the program give back the contents in json format
                if 'json' in arguments:
                    json_response = True
                    species = []
                    counter = 0
                    for specie in species_l:
                        specie_f = specie['display_name']
                        species.append(specie_f)
                        counter = counter + 1
                        if counter == limit:
                            break

                    contents = json.dumps(species)
                else:
                    json_response = False
                    contents = """
                            <html>
                            <body style="background-color: D7B7BC;"><FONT FACE="monospace" SIZE = 5 COLOR = 'white'><h3>List of the chosen limited species </h3></FONT>
                            <ol>"""
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
            except ValueError:
                answer_value = 400
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()

            except KeyError:
                answer_value = 400
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()

            except TypeError:
                answer_value = 404
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()


        elif '/karyotype' in self.path:
            try:
                arguments = self.main(self.path)
                if 'specie' in arguments and arguments['specie'] != "":
                    specie = arguments['specie']
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
                    if 'json' in arguments:
                        json_response = True
                        contents = json.dumps(karyotype_l)
                    else:
                        json_response = False
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
                else:
                    answer_value = 404
                    filename = 'error.html'
                    with open(filename, 'r') as f:
                        contents = f.read()
            except KeyError:
                answer_value = 400
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()



        elif '/chromosomeLength' in self.path:
            try:
                arguments = self.main(self.path)
                if ('specie') in arguments and ('chromo') in arguments:
                    specie = arguments['specie']
                    chromo = arguments['chromo']
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
                    if 'top_level_region' in resp:
                        info = resp['top_level_region']
                        length = 0
                        for elem in info:
                            if elem['name'] == chromo:
                                length = str(elem['length'])
                        print(length)
                        if 'json' in arguments:
                            json_response = True
                            resp_ ={'Length' : length}
                            contents = json.dumps(resp_)
                        else:
                            json_response = False
                            contents = """
                                                                                <html>
                                                                                <body style="background-color: D7B7BC;"><FONT FACE="monospace" SIZE = 5 COLOR = 'white'><h3>The length of the chromosome of the chosen specie is: </h3></FONT>
                                                                                <ul>"""


                            contents = contents + "<li>" + str(length) + "</li>"

                            """</ul>
                                                                                </body>
                                                                                </html>
                                                                                """
                    else:
                        answer_value = 404
                        filename = 'error.html'
                        with open(filename, 'r') as f:
                            contents = f.read()

                else:
                    answer_value = 404
                    filename = 'error.html'
                    with open(filename, 'r') as f:
                        contents = f.read()

            except KeyError:
                answer_value = 400
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except TypeError:
                answer_value = 400
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()

        elif '/geneSeq' in self.path:
            try:
                arguments = self.main(self.path)
                if 'gene' in arguments:
                    gene = arguments['gene']
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
                    sequence = resp['seq']
                    print(sequence)
                    if 'json' in arguments:
                        json_response = True
                        resp_ = {'Sequence': sequence}
                        contents = json.dumps(resp_)
                    else:
                        json_response = False
                        contents = """
                                                                            <html>
                                                                            <body style="background-color: D7B7BC;"><FONT FACE="monospace" SIZE = 5 COLOR = 'white'><h3>The sequence of the given human gene is: </h3></FONT>
                                                                            <ul>"""


                        contents = contents + "<li>" + sequence + "</li>"

                        """</ul>
                                                                            </body>
                                                                            </html>
                                                                  """
                else:
                    answer_value = 400
                    filename = 'error.html'
                    with open(filename, 'r') as f:
                        contents = f.read()
            except KeyError:
                answer_value = 400
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()

            except TypeError:
                answer_value = 400
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()





        elif '/geneInfo' in self.path:
            try:
                arguments = self.main(self.path)
                gene = arguments['gene']
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

                id = resp[0]['id']
                start = resp[0]['start']
                end = resp[0]['end']
                length = (end-start)+1
                chromo = resp[0]['seq_region_name']
                if 'json' in arguments:
                    json_response = True
                    resp_ = {'Id': id,'Chromo-name': chromo, 'Start': start, 'End': end, 'Length': length }
                    contents = json.dumps(resp_)
                else:
                    json_response = False
                    contents = """
                                                                    <html>
                                                                    <body style="background-color: D7B7BC;"><FONT FACE="monospace" SIZE = 5 COLOR = 'white'><h3>The information asked of the given human gene is: </h3></FONT>
                                                                    <ul>"""

                    contents = contents + "<li>" + """<FONT FACE="monospace" SIZE = 5 COLOR = 'darkslategray'><h5>The id of the sequence is: </h5></FONT>""" + str(id) + "</li>"
                    contents = contents + "<li>" + """<FONT FACE="monospace" SIZE = 5 COLOR = 'darkslategray'><h5>The start of the sequence is: </h5></FONT>""" + str(start) + "</li>"
                    contents = contents + "<li>" + """<FONT FACE="monospace" SIZE = 5 COLOR = 'darkslategray'><h5>The end of the sequence is: </h5></FONT>""" + str(end) + "</li>"
                    contents = contents + "<li>" + """<FONT FACE="monospace" SIZE = 5 COLOR = 'darkslategray'><h5>The length of the sequence is: </h5></FONT>""" + str(length) + "</li>"
                    contents = contents + "<li>" + """<FONT FACE="monospace" SIZE = 5 COLOR = 'darkslategray'><h5>The name of the gene is: </h5></FONT>""" + str(chromo) + "</li>"

                    """</ul>
                                                                        </body>
                                                                        </html>
                                                                        """

            except KeyError:
                answer_value = 400
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()

            except TypeError:
                answer_value = 400
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()

        elif '/geneCalc' in self.path:
            try:
                arguments = self.main(self.path)
                gene = arguments['gene']
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

                if 'json' in arguments:
                    json_response = True
                    s1 = Seq(sequence)
                    total_length = len(sequence)

                    pa = s1.perc('A')
                    pt = s1.perc('T')
                    pc = s1.perc('C')
                    pg = s1.perc('G')
                    resp_ = {'Sequence': sequence, 'Length': total_length, 'PercA': pa, 'PercT': pt, 'PercC': pc, 'PercG': pg}
                    print(type(resp_))
                    contents = json.dumps(resp_)

                else:
                    json_response = False
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
            except KeyError:
                answer_value = 400
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()

            except TypeError:
                answer_value = 400
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()

        elif '/geneList' in self.path:
            try:
                arguments = self.main(self.path)
                start = arguments['start']
                chromo = arguments['chromo']
                end = arguments['end']
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

                if 'json' in arguments:
                    try:
                        json_response = True
                        id_l = []
                        for elem in resp:
                            position1 = elem['feature_type']
                            if position1 == "gene":
                                position2 = elem['id']
                                id_l.append(str(position2))


                        contents = json.dumps(id_l)
                    except TypeError:
                        resp_ = 'None'
                        contents = json.dumps(resp_)
                else:
                    json_response = False
                    contents = """
                                                                    <html>
                                                                    <body style="background-color: D7B7BC;"><FONT FACE="monospace" SIZE = 5 COLOR = 'white'><h3>The names of the genes located in the chromosome asked from the start to end positions are: </h3></FONT>
                                                                    <ul>"""



                    for elem in resp:
                        #print(elem)
                        position1 = elem['feature_type']

                        if position1 == "gene":
                            position2 = elem['id']
                            print(position2)
                            contents = contents + "<li>" + 'The name of the chromosome is: ' + str(position2) + "</li>"

                        """</ul>
                                                                                </body>
                                                                                </html>
                                                                                """

            except KeyError:
                answer_value = 404
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()
            except TypeError:
                answer_value = 404
                filename = 'error.html'
                with open(filename, 'r') as f:
                    contents = f.read()



        else:
            answer_value = 404
            filename = 'error.html'
            print('prueba')
            with open(filename, 'r') as f:
                contents = f.read()



        # Generating the response message
        self.send_response(answer_value)  # -- Status line: OK!

        if (json_response == True) :
            self.send_header('Content-Type', 'application/json')
        else:
            self.send_header('Content-Type', 'text/html')

        # Define the content-type header:

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
