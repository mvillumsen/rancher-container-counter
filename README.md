# Rancher Container Counter
## Description
A small Python script that counts all running containers across all environments in Rancher 1.6 using v2 beta api. The script skips the containers running in the following stacks `healthcheck, ipsec, network-devices, scheduler` which are all internal Rancher services.
