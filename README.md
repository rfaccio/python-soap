# python-soap

### **Install suds-jurko**

`pip install suds-jurko`

### **Create config.py file**

```
wsdl = 'http://...?WSDL'
uname = ''
pwd = '' 

wsdlList = {'integrationName': {
                'url':'http://...?WSDL', 
                'response': 'integrationNameResponse'
            },
            'etc': {
                'url':'http://...?WSDL',
                'response':'etcResponse'
            }
```

Change code according to webservice definition, results may be saved in JSON format.