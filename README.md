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