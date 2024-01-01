import requests

PLANO_BASE_URL="https://planorama.arisia.org"

resp = requests.get("{}/conclar/schedule".format(PLANO_BASE_URL), verify=False)
schedule = resp.text

resp = requests.get("{}/conclar/participants".format(PLANO_BASE_URL), verify=False)
people = resp.text

with open('plano-arisia.jsonp', 'w') as f:
  f.write("var program={}\n".format(schedule))
  f.write("var people={}".format(people))
