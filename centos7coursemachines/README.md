first checkout socket_server.py
git checkout ..... different git project


please adapt the users parameter of the authorized_keys ansible module in playbook.yml to fit your system 

for provisioning to work you need to run 
```
vagrant up
```

and never only a single machine or a subset of machines

otherwise provisioning of the machines using ansible will not work

if you want to use passwordless ssh for root user, copy the users ssh pubkey your running vagrant to the root users .root/id_rsa and .root/id_rsa.pub
