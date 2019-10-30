import json
import operator
from datetime import datetime
import zeep
from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep.transports import Transport
from zeep.wsse.username import UsernameToken

import config

#url = WSDL url
#data = SOAPrequest parameters
def send_request(url, data):
    wsdlMethods = []

    #authentication and client initialization
    session = Session()
    session.auth = HTTPBasicAuth(config.uname,config.pwd)
    transport = Transport(session=session)
    client = zeep.Client(url, transport=transport)

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

    #client.service.[METHOD](<parameters>)

    #check if method signature contains specific parameters
    if 'dataUltimoEnvio' in signature:
        r = getattr(client.service, wsdlMethods[0])(data['dataUltimoEnvio'],data['ultimoRegistro']) #getattr dynamically calls a method from the WSDL structure inspected above
    elif 'ultimoRegistro' in signature:
        r = getattr(client.service, wsdlMethods[0])(data['ultimoRegistro'])
    else:
        r = None
    return r

#test cases
# 0 = Simple SOAP teste with one WSDL
if input('Simple test [0] or Octopus Test? [1]:> ') == '0':
    #SOAPrequest parameters
    req_data = {'dataUltimoEnvio': '1999-01-01',
                'ultimoRegistro': '0'}

    r = send_request(config.wsdlList['localInstalacao']['url'], req_data)

    print(r['localInstalacaoResponse'])
    input_dict = zeep.helpers.serialize_object(r)
    js = json.dumps(input_dict, indent=4)
    filename = 'localInstalacao-' + str(r['nRegistro']) + '.json'
    SOAPresponse = open(filename, 'a')
    SOAPresponse.write(js)
    SOAPresponse.close()

# 1 = Full Octopus test
else:
    #config.octopusList contains multiple WSDL urls
    for index, (wsdlName, wsdlAttributes) in enumerate(config.wsdlList.items()):
        #SOAPrequest parameters
        req_data = {'dataUltimoEnvio': '1999-01-01',
                    'ultimoRegistro': '0'}

        while True:
            print('\n----- %s -----' % datetime.now())
            r = send_request(wsdlAttributes['url'], req_data)

            if r != None:
                print('nRegistro: ', r['nRegistro'])
                print('Total Registros: ', r['totalRegistros'])

                input_dict = zeep.helpers.serialize_object(r)
                js = json.dumps(input_dict, indent=4)
                filename = 'results/' + str(index) + '-' + wsdlName + '-' + str(r['nRegistro']) + '.json'
                SOAPresponse = open(filename, 'a')
                SOAPresponse.write(js)
                SOAPresponse.close()
                print('\n----- %s -----\n' % datetime.now())
                req_data['ultimoRegistro'] = r['nRegistro']

                if r['nRegistro'] == r['totalRegistros']:
                    req_data['ultimoRegistro'] = '0'
                    break
            else:
                break
