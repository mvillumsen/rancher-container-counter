import urllib.request
import json
from config import *

# Setup authentication for urllib
passMgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
passMgr.add_password(None, RANCHER_URL, RANCHER_API_USERNAME, RANCHER_API_PASSWORD)
authHandler = urllib.request.HTTPBasicAuthHandler(passMgr)
urlOpener = urllib.request.build_opener(authHandler)
urllib.request.install_opener(urlOpener)

with urllib.request.urlopen(RANCHER_URL + "projects/") as url:
    ignore = ['healthcheck', 'ipsec', 'network-services', 'scheduler']
    counter_prod = 0
    counter_nonprod = 0
    data = json.loads(url.read().decode())
    json_data = data['data']

    for env in json_data:
        prod = 'production' in env['name']
        with urllib.request.urlopen(RANCHER_URL + "projects/" + env['id'] + "/instances") as instances:
            instances_data = json.loads(instances.read().decode())['data']

            # Ignore Rancher's internal services
            user_instances = list(filter(lambda x: 'io.rancher.stack.name' in x['labels'] and x['labels']['io.rancher.stack.name'] not in ignore, instances_data))

            if prod:
                counter_prod += len(user_instances)
            else:
                counter_nonprod += len(user_instances)

    print("Containers running in production:", counter_prod)
    print("Containers running in non-production:", counter_nonprod)
    print("Containers running in total:", counter_prod + counter_nonprod)

