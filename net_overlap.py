#!/usr/bin/env python
import ipaddress
from azure.identity import AzureCliCredential
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest
from azure.mgmt.resource import SubscriptionClient
from pprint import pprint
import argparse


def is_valid_ipv4_network(input_str):
    try:
        ipaddress.ip_network(input_str, strict=False)
        return True
    except ValueError:
        return False


# Instantiate the argument parser
parser = argparse.ArgumentParser(description='Calculate if an IPv4 CIDR overlaps with an existing Azure VNet')
# Required positional argument
parser.add_argument('input_network', type=str,
                    help='example: 10.1.0.0/16')
# Switch
parser.add_argument('--verbose', action='store_true',
                    help='print extra information')
args = parser.parse_args()

# convert input string to ip_network type
if is_valid_ipv4_network(args.input_network):
    input_network = ipaddress.ip_network(args.input_network, strict=False)
else:
    raise argparse.ArgumentTypeError(f'{args.input_network} is not a valid IPv4 CIDR')


# Authenticate to Azure
credential = AzureCliCredential()

# Instantiate a Resource Graph client
client = ResourceGraphClient(credential)


def get_subscriptions():
    # Instantiate a Subscription client
    client = SubscriptionClient(credential)

    # Retrieve subscriptions and save them to a list
    subscription_ids = [subscription.subscription_id for subscription in client.subscriptions.list()]

    # Print the subscription IDs
    if args.verbose:
        print(f'Found {len(subscription_ids)} subscriptions\n')
        for sub_id in subscription_ids:
            print(sub_id)
        print()
    return subscription_ids


# get ALL subscriptions
subscriptions = get_subscriptions()

# Define the query
q = "Resources | where type =~ 'Microsoft.Network/virtualNetworks' | project name, addressSpace = properties.addressSpace.addressPrefixes"
query = QueryRequest(query=q)
query.subscriptions = subscriptions

# Run the query
response = client.resources(query).as_dict()
vnets = response['data']
if args.verbose:
    print(f'Found {len(vnets)} VNets\n')
    pprint(vnets)
    print()

for vnet in vnets:
    for cidr in vnet['addressSpace']:
        ip_network = ipaddress.ip_network(cidr)
        overlap = input_network.overlaps(ip_network)
        if overlap:
            print(f'{input_network} overlaps {vnet}')