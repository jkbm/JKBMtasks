import requests
import json
import sys

args = sys.argv

ACCESS_TOKEN = "bea8698781bf4afc84bb419683a91512"

url = "http://data.fixer.io/api/latest?access_key={0}".format(ACCESS_TOKEN)


r = requests.post(url=url)
jr = json.loads(r.text)

EUR = 1

def get_rates(ammount=100, curr1="USD", curr2="UAH"):
    try:
        cbuy = jr['rates'][curr2]/jr['rates'][curr1]
        report = "{0}{1} to equals to {3}{2}".format(amount, curr1, curr2, round(float(amount)*cbuy, 2))
    except:
        report = "Wrong arguments"
        print("Available values: {0}".format([x for x in jr['rates'].keys()]))

    return report