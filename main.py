from suds.client import Client
import json
import config

wsdl = config.wsdl
uname = config.uname
pwd = config.pwd

client = Client(wsdl, username=uname, password=pwd)

# parametros de controle deste webservice especifico
nRegistro = 0
totalRegistros = 0
tabela = {}

while True:
    #service.[NOME DO METODO]
    result = client.service.SI_DadoMestre_LocInstalacao_Octopus_Sync_Out('1999-01-01',nRegistro)

    #controle de execução fracionada deste webservice
    ultimoRegistro = nRegistro
    nRegistro = result.nRegistro
    totalRegistros = result.totalRegistros

    print('\n\n----------------------------')
    print('nRegistro: ', nRegistro)
    print('totalRegistros: ', totalRegistros)
    print('----------------------------\n\n')

    for line, value in enumerate(result.localInstalacaoResponse):
        indice = line + 1 + ultimoRegistro
        
        item = {'status': value.status, 
                'localInstalacao': value.localInstalacao, 
                'descricao': value.descricao, 
                'centro': value.centro, 
                'tipoObjeto': value.tipoObjeto, 
                'grupoPlanejamento': value.grupoPlanejamento}

        print(indice, value.descricao)
        tabela[indice] = item

    if result.nRegistro == result.totalRegistros:
        # print(json.dumps(tabela,indent=4))
        break

js = json.dumps(tabela)
arquivo = open('resultado.json', 'a')
arquivo.write(js)
arquivo.close()