# Cisco_EoX_Api
Script simples para extrair informações do Smartnet Total Care EOX API

## Requirimentos

Essa aplicaço requer acesso à "EOX API", que encontra-se em [https://apiconsole.cisco.com/](https://apiconsole.cisco.com/).
Essa API é mantida pelo SNTC (Smart Net Total Care Service).

Para ter acesso ao "EOX API", é necessário seguir se registrar na cisco. Seu registro precisa estar vinculado à uma organização que tenha o serviço de Smart Net Total Care Service. Após vincular, basta criar uma nova aplicação dentro do API CONSOLE, e obter o dados como "Client_id" e "Client_secret".

Os detalhes da API se encontram também na documentação que se encontra no link a seguir: [https://developer.cisco.com/docs/support-apis/#!eox](https://developer.cisco.com/docs/support-apis/#!eox)

## Como usar ?

cisco_eox_api é bem simples de entender, e permite que você consiga apartir dele construir aplicações que consigam tratar essas informações.

Abaixo um exemplo:

```
{
        "Product_id": "Catalyst 3560 48 10/100 + 4 SFP IPB Image", 
        "EndOfSvcAttachDate": "2011-07-05", 
        "EoS_Alert": "critical", 
        "LastDateOfSupport": "2015-07-31", 
        "EOXMigrationDetails": "WS-C3560V2-48TS-S", 
        "EndOfSaleDate": "2010-07-05", 
        "ServiceContractRenewal_Alert": "critical", 
        "EndOfSWMaintenanceReleases": "2013-07-04", 
        "Serial_Number": "CAT1038NHFB", 
        "EndOfServiceContractRenewal": "2014-09-30", 
        "EndOfRoutineFailureAnalysisDate": "2011-07-05"
}
```
Como podemos analisar o output que é retornado na API, nos trás diversas informações, e com elas é possivel implementar um Dashboard, construir graficos, e servir como um auxílio ao Smart Net Total Care Service.

Obrigado, e qualquer dúvida só contactar !!!
