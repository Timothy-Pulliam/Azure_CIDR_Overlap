## Setup

```bash
az login
git clone git@github.com:Timothy-Pulliam/Azure_CIDR_Overlap.git
cd Azure_CIDR_Overlap
python3 -m venv venv
. venv/bin/activate
pip install -U pip
pip install -r requirements
```

## Usage

The script will pull all VNets from all Subscriptions (that the user has access to)
using an Azure Resource Graph Explorer query.

Pass an IPv4 CIDR as a positional argument. No output indicates the provided CIDR does not overlap with any existing VNets.

```bash
$ ./net_overlap.py '12.34.56.78/16'
$
```

If the CIDR does overlap, it will list the overlapping VNets

```bash
$ ./net_overlap.py '10.0.0.0/16'
10.0.0.0/16 overlaps {'name': 'vnet-myapp-dev-1', 'addressSpace': ['10.0.0.0/16']}
```

Optionally, run in verbose mode

```bash
$ ./net_overlap.py '10.2.0.0/16' --verbose
Found 1 subscriptions

xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Found 2 VNets

[{'addressSpace': ['10.0.0.0/16'], 'name': 'vnet-myapp-dev-1'},
 {'addressSpace': ['10.1.0.0/16', '10.2.0.0/16'], 'name': 'vnet-myapp-dev-2'}]

10.2.0.0/16 overlaps {'name': 'vnet-myapp-dev-2', 'addressSpace': ['10.1.0.0/16', '10.2.0.0/16']}
```
