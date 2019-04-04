# Setup Node Cluster with Queue Mirroring #
This guide details the process to setup a node cluster with a mirrored queue (high availability) on Windows.

## Configure a Single Node 

- Install Erlang and RabbitMQ Server as Administrator
- Run RabbitMQ Service -start from Start Menu
- Confirm the RabbitMQ service description is appearing in Services. If it is blank, the install did not finish successfully.
- Navigate to C:\Program Files\RabbitMQ Server\rabbitmq_server-x.x.xx\sbin
- Check the value of the *%HOMEDRIVE%* environmental variable. If not set to a local path, set the location to a local drive:

> set HOMEDRIVE=C:\Users\jowens\AppData\Roaming\RabbitMQ

- Start RabbitMQ:
> rabbitmq-server -detached

- Verify the local node is running:
> rabbitmqctl cluster_status

- Enable RabbitMQ Management UI:
> rabbitmq-plugins enable rabbitmq_management
 
>sc stop RabbitMQ

>sc start RabbitMQ

- Login to the Management UI via

> http://localhost:15672/#/

- Navigate to Queues > Add Queue
- Enter a queue name and select "Add Queue"
- Repeat the above steps to setup RabbitMQ nodes on all necessary machines

## Setup a Cluster 

- After setting up multiple nodes, we are ready to setup a cluster
- Login to the server that will be setup as master
- Copy the .erlang.cookie from: 

> %HOMEDRIVE%

**Important**: If the RabbitMQ service is not running from the NT default system account, the first .erlang.cookie file will be saved instead to %USERPROFILE%

- Login to each secondary node(s) and run: 

> rabbitmqctl stop_app

- Delete the existing .erlang.cookie from the following locations if it exists:

> C:\Windows\System32\config\systemprofile 
%HOMEDRIVE%
%USERPROFILE%

- Paste the copied .erlang.cookie into the above directories
- From the master node, copy the cluster name:

> rabbitmqctl cluster_status

- On each secondary node, run the following command to join the cluster

> rabbitmqctl join_cluster rabbit@CLUSTERNAME

- Start RabbitMQ on each secondary node

> rabbitmqctl start_app

- Verify the secondary nodes have joined the cluster:

> rabbitmqctl cluster_status

## Setup High Availability Policy (Queue Mirroring)

- Login to the management UI on the master node via

> http://localhost:15672/#/

- Navigate to Admin >Policies > Add Policy
- Enter a name for the policy
- Enter the queue name under "Pattern"
- Set the definition to "HA" with key "All"
- Select "Add Policy"
- From each secondary node, synchronize the queue:

> rabbitmqctl sync_queue QUEUENAME

## Summary

We now have a group of nodes inside of a cluster that all share the same queue and exchange. If any node fails, the messages will still be stored across the remaining nodes within the cluster. If the master node is to fail, the secondary node with the longest uptime will automatically takeover as master.
