import requests
import json
import sys

args = sys.argv

ACCESS_TOKEN = "bea8698781bf4afc84bb419683a91512"

url = "http://data.fixer.io/api/latest?access_key={0}".format(ACCESS_TOKEN)

def get_rates(amount=100, curr1="USD", curr2="UAH"):
    r = requests.post(url=url)
    jr = json.loads(r.text)
    try:
        cbuy = jr['rates'][curr2]/jr['rates'][curr1]
        report = "{0}{1} equals to {3}{2}".format(amount, curr1, curr2, round(float(amount)*cbuy, 2))
    except Exception as e:
        report = e
        print("Available values: {0}".format([x for x in jr['rates'].keys()]))
    
    return report
