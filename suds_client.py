# This Python file uses the following encoding: utf-8

from suds.client import Client
import json
import config

# file config.py contains WSDL url and authentication info
wsdl = config.wsdl
username = config.uname
password = config.pwd
wsdlMethods = []

client = Client(wsdl, username=username, password=password)

#list all available methods
for method in client.wsdl.services[0].ports[0].methods.values():
    wsdlMethods.append(method.name)
    print('%s(%s)' % (method.name, ', '.join('%s: %s' % (part.type, part.name) for part in method.soap.input.body.parts)))

# variables specific to this WebService scenario:
nRegistro = 0
totalRegistros = 0
dateValue = '1999-01-01'
result = {}

while True:
    #service.[METHOD], this changes with every webservice
    print(wsdlMethods[0])
    SOAPresponse = getattr(client.service, wsdlMethods[0])(dateValue,nRegistro)
    #SOAPresponse = client.service.SI_DadoMestre_LocInstalacao_Octopus_Sync_Out(dateValue,nRegistro)

    #WHILE flow control
    ultimoRegistro = nRegistro
    nRegistro = SOAPresponse.nRegistro
    totalRegistros = SOAPresponse.totalRegistros

    # Success messages
    print('\n\n----------------------------')
    print('nRegistro: ', nRegistro)
    print('totalRegistros: ', totalRegistros)
    print('----------------------------\n\n')

    # Add SOAPResponse attributes to result structure
    for line, value in enumerate(SOAPresponse.localInstalacaoResponse):
        indice = line + 1 + ultimoRegistro

        item = {'status': value.status, 
                'localInstalacao': value.localInstalacao, 
                'descricao': value.descricao, 
                'centro': value.centro, 
                'tipoObjeto': value.tipoObjeto, 
                'grupoPlanejamento': value.grupoPlanejamento}

        print(indice, value.descricao)
        result[indice] = item

    if nRegistro == totalRegistros:
        # print(json.dumps(result,indent=4))
        break

js = json.dumps(result)
arquivo = open('result.json', 'a')
arquivo.write(js)
arquivo.close()
print('\n\n----------------------------')
print('Response saved: ', 'result.json')
print('----------------------------\n\n')
