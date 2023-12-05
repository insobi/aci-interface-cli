[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/insobi/ndfc-template-cli)

# ACI Interface CLI
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

Display how to use
```
Usage: aci-interface-cli.py list [OPTIONS]

  Show a list of Physical Interfaces from ACI

Options:
  --table / --json  Show a list as table or json
  --csv             Download csv file of interfaces
  --help            Show this message and exit.
```

check out Physical Interface as table
```bash
$ python aci-interface-cli.py list
+-----+------+-----------+---------+------+-------+-------------------+
| pod | node | interface | adminSt | mtu  | mode  | descr             |
+-----+------+-----------+---------+------+-------+-------------------+
| 1   | 1201 | eth1/1    | up      | 9000 | trunk | test1             |
| 1   | 1201 | eth1/2    | up      | 9000 | trunk | test2             |
| 1   | 1201 | eth1/3    | up      | 9000 | trunk | test3             |
| 1   | 1201 | eth1/4    | up      | 9000 | trunk | test4             |
...
```

Or check out Physical Interface as JSON
```bash
$ python aci-interface-cli.py list --json

...
```

Download csv file for list of Physical Interface
```bash
$ python aci-interface-cli.py list --csv

interface.csv file was created.
```