import zeep
import operator
from zeep.wsse.username import UsernameToken
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from requests import Session
from zeep.transports import Transport
import json
import config

#integration = name of SOAP integration to be used, contains 'url' and 'response' attributes
#data = SOAPrequest parameters
def send_request(integration, data):
    #get wsdl information from config.py file
    #wsdl = config.wsdlList[integration]
    wsdlMethods = []

    #authentication and client initialization
    session = Session()
    session.auth = HTTPBasicAuth(config.uname,config.pwd)
    transport = Transport(session=session)
    client = zeep.Client(config.wsdlList[integration]['url'], transport=transport)

    #get method names
    for service in client.wsdl.services.values():
        print("service:", service.name)
        for port in service.ports.values():
            operations = sorted(
                port.binding._operations.values(),
                key=operator.attrgetter('name'))

            for operation in operations:
                wsdlMethods.append(operation.name)
                signature = operation.input.signature()

    #check if method signature contains specific parameters
    #client.service.[METHOD](<parameters>)
    #getattr dynamically calls a method from the WSDL structure inspected above
    if 'dataUltimoEnvio' in signature:
        r = getattr(client.service, wsdlMethods[0])(req_data['dataUltimoEnvio'],req_data['ultimoRegistro'])
    elif 'ultimoRegistro' in signature:
        r = getattr(client.service, wsdlMethods[0])(req_data['ultimoRegistro'])
    else:
        r = None
    return r

#test cases
# 0 = Simple SOAP teste with one WSDL
if input('Simple test [0] or Octopus Test? [1]: >') == '0':
    #SOAPrequest parameters
    req_data = {'dataUltimoEnvio': '1999-01-01',
                'ultimoRegistro': '0'}
    r = send_request('localInstalacao', req_data)
    print(r['localInstalacaoResponse'])

# 1 = Full Octopus test
else:
    #config.octopusList contains multiples WSDL urls
    for n, integration in enumerate(config.wsdlList):
        #SOAPrequest parameters
        req_data = {'dataUltimoEnvio': '1999-01-01',
                    'ultimoRegistro': '0'}

        while True:
            r = send_request(integration, req_data)
            if r != None:
                print('nRegistro: ', r['nRegistro'])
                print('Total Registros: ', r['totalRegistros'])
                response = str([r[config.wsdlList[integration]['response']]])

                filename = 'results/' + str(n) + '-' + integration + '-' + str(r['nRegistro']) + '.txt'
                arquivo = open(filename, 'a')
                arquivo.write(response)
                arquivo.close()

                req_data['ultimoRegistro'] = r['nRegistro']

                if r['nRegistro'] == r['totalRegistros']:
                    req_data['ultimoRegistro'] = '0'
                    break
            else:
                break
