# Multinet operator

## Description

This is an operator example for validating multiple interfaces using Multus

## Prepare environment

For preparing the environment we need to install and configure our favorite K8s, Juju, and Charmcraft.

Microk8s:

```bash
sudo snap install microk8s --classic --channel 1.20/stable
mkdir -p ~/.kube
sudo usermod -a -G microk8s `whoami`
sudo chown -f -R `whoami` ~/.kube
newgrp microk8s
microk8s.status --wait-ready
microk8s.enable storage multus dns
```

Juju:

```bash
sudo snap install juju --classic --channel 2.8/stable
juju bootstrap microk8s
juju add-model test-multinet
```

Charmcraft:

```bash
sudo snap install charmcraft --beta
```

## Testing

## Create NetworkAttachmentDefinition

The following command will create two networks (net1 and net2) attached to the `wlo1` interface in the host machine.

Change the name of the interface in `specs/networks.yaml` if you want to change it to another interface.

```bash
microk8s.kubectl apply -f specs/networks.yaml -n test-multinet
```

## Deploy

Build charm:

```bash
charmcraft build
```

Deploy:

```bash
juju deploy ./multinet.charm --config networks=net1,net2:eth2 --config static_ips=net2:10.222.222.225 multinet1

juju deploy ./multinet.charm --config networks=net1,net2:eth2 multinet2
```

Validate:

```bash
$ microk8s.kubectl -n test-multinet get pods

NAME                             READY   STATUS    RESTARTS   AGE
modeloperator-6774bff484-p4f9v   1/1     Running   0          27m
multinet1-operator-0             1/1     Running   0          22s
multinet2-operator-0             1/1     Running   0          20s
multinet1-658b645988-dwm8v       1/1     Running   0          16s
multinet2-656798c965-rh8g9       1/1     Running   0          12s
$ microk8s.kubectl -n test-multinet logs multinet1-658b645988-dwm8v
eth0      Link encap:Ethernet  HWaddr 6E:BF:E2:10:7F:43  
          inet addr:10.1.245.69  Bcast:0.0.0.0  Mask:255.255.255.255
          inet6 addr: fe80::6cbf:e2ff:fe10:7f43/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1440  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:11 errors:0 dropped:1 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:0 (0.0 B)  TX bytes:866 (866.0 B)

eth2      Link encap:Ethernet  HWaddr 9A:C6:A7:5B:8D:75  
          inet addr:10.222.222.225  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::98c6:a7ff:fe5b:8d75/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:92 errors:0 dropped:0 overruns:0 frame:0
          TX packets:14 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:5725 (5.5 KiB)  TX bytes:1088 (1.0 KiB)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

net1      Link encap:Ethernet  HWaddr B6:F3:2E:57:07:A9  
          inet addr:10.111.111.129  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::b4f3:2eff:fe57:7a9/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:93 errors:0 dropped:0 overruns:0 frame:0
          TX packets:14 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:5781 (5.6 KiB)  TX bytes:1088 (1.0 KiB)
$ microk8s.kubectl -n test-multinet logs multinet2-656798c965-rh8g9
eth0      Link encap:Ethernet  HWaddr F2:C9:09:39:80:11  
          inet addr:10.1.245.121  Bcast:0.0.0.0  Mask:255.255.255.255
          inet6 addr: fe80::f0c9:9ff:fe39:8011/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1440  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:9 errors:0 dropped:1 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:0 (0.0 B)  TX bytes:726 (726.0 B)

eth2      Link encap:Ethernet  HWaddr 0A:1D:C1:A2:E8:D1  
          inet addr:10.222.222.226  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::81d:c1ff:fea2:e8d1/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:20 errors:0 dropped:0 overruns:0 frame:0
          TX packets:13 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:1260 (1.2 KiB)  TX bytes:1018 (1018.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

net1      Link encap:Ethernet  HWaddr 42:EA:15:E0:A9:D2  
          inet addr:10.111.111.130  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::40ea:15ff:fee0:a9d2/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:21 errors:0 dropped:0 overruns:0 frame:0
          TX packets:12 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:1316 (1.2 KiB)  TX bytes:948 (948.0 B)
```

The previous logs show the ifconfig of the pods. Both should have an interface with the name `net1` connected to the network `net1` defined in `specs/networks.yaml`, and another interface `eth2` connected to the `net2` network. 

Checks:
- multinet1:
    - net1:
        - IP range: 10.111.111.0/24
    - eth2:
        - IP: 10.222.222.225
- multinet2:
    - net1:
        - IP range: 10.111.111.0/24
    - eth2:
        - IP range: 10.222.222.0/24
