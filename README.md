# ACI Interface CLI

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/insobi/aci-interface-cli)

A Command Line Interface designed for retrieving interfaces from Cisco ACI

## Installation

Clone the repo
```bash
git clone https://github.com/insobi/aci-interface-cli.git
```
Go to your project folder
```bash
cd aci-interface-cli
```

Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

Set environment variables
```bash
export ACI_USERNAME="admin"
export ACI_PASSWORD="C1sco12345"
export ACI_URL="https://198.18.133.200"
```

How to use
```
Usage: aci-interface-cli.py [OPTIONS] COMMAND [ARGS]...

  ACI Interface CLI

Options:
  --help  Show this message and exit.

Commands:
  phys  Shows physical interfaces
  vpc   Shows vpc interfaces
```

How to use phys command
```
Usage: aci-interface-cli.py phys [OPTIONS]

  Shows physical interfaces

Options:
  --state [up|down]  Filter by adminSt of interface
  --csv              Downloads as csv file
  --descr-exists     Including only interfaces having description
  --raw              Shows raw data as json format
  --help             Show this message and exit.
```

Check out Physical Interface as table
```bash
$ python aci-interface-cli.py phys
+-----+------+-----------+---------+------+-------+-------------------+
| pod | node | interface | adminSt | mtu  | mode  | descr             |
+-----+------+-----------+---------+------+-------+-------------------+
| 1   | 1201 | eth1/1    | up      | 9000 | trunk | hello             |
| 1   | 1201 | eth1/2    | up      | 9000 | trunk | world             |
| 1   | 1201 | eth1/3    | up      | 9000 | trunk |                   |
| 1   | 1201 | eth1/4    | up      | 9000 | trunk |                   |
...
+-----+------+-----------+---------+------+-------+-------------------+
```

Check out only physical Interface which have description
```bash
$ python aci-interface-cli.py phys --descr-exists
+-----+------+-----------+---------+------+-------+-------------------+
| pod | node | interface | adminSt | mtu  | mode  | descr             |
+-----+------+-----------+---------+------+-------+-------------------+
| 1   | 1201 | eth1/1    | up      | 9000 | trunk | hello             |
| 1   | 1201 | eth1/2    | up      | 9000 | trunk | world             |
+-----+------+-----------+---------+------+-------+-------------------+
```

Download a csv file for list of Physical Interface
```bash
$ python aci-interface-cli.py phys --csv

interface_phys.csv file was created.
```

Check out interface list filtered by json query with --raw option and jq
```
$ python aci-interface-cli.py phys --raw | jq '.imdata[].l1PhysIf.attributes | select(.mode|contains("trunk"))'
{
  "adminSt": "up",
  "autoNeg": "on",
  "breakT": "nonbroken",
  "bw": "0",
  "childAction": "",
  "delay": "1",
  "descr": "",
  "dfeDelayMs": "0",
  "dn": "topology/pod-2/node-2201/sys/phys-[eth1/32]",
  "dot1qEtherType": "0x8100",
  "emiRetrain": "disable",
  "enablePoap": "no",
  "ethpmCfgFailedBmp": "",
  "ethpmCfgFailedTs": "00:00:00:00.000",
  "ethpmCfgState": "0",
  "fcotChannelNumber": "Channel32",
  "fecMode": "inherit",
  "id": "eth1/32",
  "inhBw": "unspecified",
  "isReflectiveRelayCfgSupported": "Supported",
  "layer": "Layer2",
  "lcOwn": "local",
  "linkDebounce": "100",
  "linkFlapErrorMax": "30",
  "linkFlapErrorSeconds": "420",
  "linkLog": "default",
  "mdix": "auto",
  "medium": "broadcast",
  "modTs": "2023-10-21T19:56:51.655+00:00",
  "mode": "trunk",
  "monPolDn": "uni/infra/moninfra-default",
  "mtu": "9000",
  "name": "",
  "pathSDescr": "",
  "portPhyMediaType": "auto",
  "portT": "leaf",
  "prioFlowCtrl": "auto",
  "reflectiveRelayEn": "off",
  "routerMac": "not-applicable",
  "snmpTrapSt": "enable",
  "spanMode": "not-a-span-dest",
  "speed": "inherit",
  "status": "",
  "switchingSt": "disabled",
  "trunkLog": "default",
  "usage": "discovery"
},
...
```