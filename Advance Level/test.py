import http.client
import json
import termcolor

PORT = 8000
SERVER = 'localhost'

print("\nConnecting to server: {}:{}\n".format(SERVER, PORT))

# Connect with the server
conn = http.client.HTTPConnection(SERVER, PORT)

conn.request("GET", "/listSpecies?limit=9&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
print("List of species:")
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)

conn.request("GET", "/karyotype?specie=gorilla&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
print("Karyotype of the given gene: ")
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)

conn.request("GET", "/chromosomeLength?specie=mouse&chromo=1&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
data1 = r1.read().decode("utf-8")
print("Chromosome Length: ")
response = json.loads(data1)
print (response)

conn.request("GET", "/geneSeq?gene=FRAT1&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
print("Gene seq")
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)

conn.request("GET", "/geneInfo?gene=FRAT1&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
print("Gene info:")
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)

conn.request("GET", "/geneCal?gene=FRAT1&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
print("Gene calculations:")
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)


#REVISAR ESTE PORQUE EL DICCIONARIO QUE ME DEVUELVE ESTA MAL
conn.request("GET", "/geneList?chromo=1&start=1&end=30000&json=1")
r1 = conn.getresponse()
print("Response received!: {} {}\n".format(r1.status, r1.reason))
print("Gene list:")
data1 = r1.read().decode("utf-8")
response = json.loads(data1)
print(response)



