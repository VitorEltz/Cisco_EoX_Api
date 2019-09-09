import requests
import json, os, fnmatch
import datetime
import time
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

# A Funcao abaixo gera o token de acesso, utilizando o client_id e client_secret, enviando um "POST" na API, retornando um token de autenticacao
def get_access_token(client_id, client_secret):

    url = "https://cloudsso.cisco.com/as/token.oauth2"
    payload = "grant_type=client_credentials&client_id="+client_id+"&client_secret="+client_secret

    headers = {
        'accept': "application/json",
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    if (response.status_code == 200):
        return response.json()['access_token']
    else:
        response.raise_for_status()

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

# Esta funcao tem como objetivo pegar o "access_token" e os "serialnumber" para fazer o "GET" na API, assim retornando um json
def get_eox_details(access_token,serialnumber):
    url = "https://api.cisco.com/supporttools/eox/rest/5/EOXBySerialNumber/1/" + serialnumber + "?responseencoding=json"

    headers = {
        'authorization': "Bearer " + access_token,
        'accept': "application/json",
    }
    response = requests.request("POST", url, headers=headers)
    if (response.status_code == 200):
        return json.loads(response.text)
    else:
        response.raise_for_status()
        return ""

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
# Esta funcao tem o objetivo de realizar um calculo que trara 4 tipos de resulto, sao eles:
# Critical = Quer dizer que o dispositivo esta expirado
# High = Em 3 meses seu dispositivo ficara expirado
# Medium = Em 6 meses seu dispositivo ficara expirado
# Normal = Seu dispositovo esta com o tempo regular n


def timestamp_calc_function(string_test):
    ts_now = int(time.time())

    ts_get = int(time.mktime(datetime.datetime.strptime(string_test, "%Y-%m-%d").timetuple()))

    ts_result = ts_get - ts_now

    if ts_result < 0 :
        state = 'critical'

    if ts_result > 0 and  ts_result <= 7776000:
        state = 'high'

    if ts_result > 7776000 and  ts_result <= 15552000:
        state = 'medium'

    if   ts_result > 15552000:
        state = 'normal'
    return state


################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
# Nesta area temos os seguintes parametros: client_id e client_secret
# Para gerar o client_id e client_secret, acesse o site "https://apiconsole.cisco.com/" e registre uma "New_Application", selecione API_EOX_v5.



client_id = 'mjp4rd26r5ccq39gevm42293' #Aqui coloque o client_id. Ex: 'sadasdadsadsafsdfsdfsfdsf' (coloque entre o codigo aspas simples)
client_secret = 'mwUVKYyB7jRtPjZRgwzuQa24' #Aqui coloque o client_secret. Ex: 'sadasdadsadsafsdfsdfsfdsf' (coloque entre o codigo aspas simples)

#Aqui chama funcao que pega o token de autenticacao
access_token = get_access_token(client_id,client_secret)

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
#Caminho da pasta onde o arquivo "serial_numbers".json fica.
folder_base = '/opt/Harpia/assesment/'
list_final = []

#Percorre o caminho de pastas ate encontrar o arquivo serial_number.json
for root, dirnames, filenames in os.walk(folder_base):
    #break
    for filename in fnmatch.filter(filenames, 'serial_numbers.json'):
        file = os.path.join(root, filename)
        with open(file, 'r') as fp:
            #Carrega a lista que contem os "serial_numbers" dentro de "fp"
            data = json.load(fp)
            #data = ['CAT0923R13H']
            #Aqui para cada serial_number ele chama funcao "get_eox_details" e retornara uma lista de objetos da API
            for serialnumber in data:
                dict_temp = {}
                print_eox = get_eox_details(access_token, serialnumber)
                #Abaixo apos o retorno da lista, vamos pegar as informacoes relevantes
                dict_temp['Serial_Number'] = serialnumber
                dict_temp['Product_id'] = print_eox['EOXRecord'][0]['ProductIDDescription']
                dict_temp['EndOfSaleDate'] = print_eox['EOXRecord'][0]['EndOfSaleDate']['value']
                dict_temp['EndOfSWMaintenanceReleases'] = print_eox['EOXRecord'][0]['EndOfSWMaintenanceReleases']['value']
                dict_temp['EndOfRoutineFailureAnalysisDate'] = print_eox['EOXRecord'][0]['EndOfRoutineFailureAnalysisDate']['value']
                dict_temp['EndOfServiceContractRenewal'] = print_eox['EOXRecord'][0]['EndOfServiceContractRenewal']['value']
                dict_temp['LastDateOfSupport'] = print_eox['EOXRecord'][0]['LastDateOfSupport']['value']
                dict_temp['EndOfSvcAttachDate'] = print_eox['EOXRecord'][0]['EndOfSvcAttachDate']['value']
                dict_temp['EOXMigrationDetails'] = print_eox['EOXRecord'][0]['EOXMigrationDetails']['MigrationProductId']

                if dict_temp['EndOfSaleDate'] == "" and dict_temp['EndOfServiceContractRenewal'] == "":
                    dict_temp['EndOfSaleDate'] = 'None'
                    dict_temp['EndOfServiceContractRenewal'] = 'None'
                else:
                    status_eox = timestamp_calc_function(dict_temp['EndOfSaleDate'])
                    dict_temp['EoS_Alert'] = status_eox
                    status_eox = timestamp_calc_function(dict_temp['EndOfServiceContractRenewal'])
                    dict_temp['ServiceContractRenewal_Alert'] = status_eox

                #Aqui apenas pegamos o "dict_temp" que carrega as informacoes necessarias, e concatena as informacoes na "list_final"
                list_final.append(dict_temp)


################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
#Nessa sessao apenas vamos salvar o resultado do list_final e gerar um json
result = '/opt/Harpia/assesment/result_json/node_hardware_eox.json'
with open(result, 'w') as fp:
    json.dump(list_final, fp, indent=4)