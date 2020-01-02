import time

import docker



client = docker.from_env()

testnet = client.networks.create('test-network', driver='bridge')
c1 = client.containers.run('debian', 'sleep 100', detach=True)
c2 = client.containers.run('debian', 'sleep 100', detach=True)
testnet.connect(c1, aliases=['c1'])
testnet.connect(c2, aliases=['c2'])

print(c1.name)
print(c2.name)

time.sleep(3)


#c2 = client.containers.run('debian', 'ping ')