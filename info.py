#!/usr/bin/env python3

import sys
from meshtastic.tcp_interface import TCPInterface
from meshtastic.util import message_to_json, convert_mac_addr, remove_keys_from_dict
import json


if len(sys.argv) < 2:
    print("Usage: python info.py <host>")
    sys.exit(1)


host=sys.argv[1]

node = TCPInterface(host)

def createInfoJson(self) -> str:  # pylint: disable=W0613
    """Generate JSON output"""

    data = {}
    data["owner"] = f"{self.getLongName()} ({self.getShortName()})"

    if self.metadata:
        data["metadata"] = json.loads(f"{message_to_json(self.metadata)}")
    
    nodes = {}
    if self.nodes:
        for n in self.nodes.values():
            keys_to_remove = ("raw", "decoded", "payload")
            n2 = remove_keys_from_dict(keys_to_remove, n)

            # if we have 'macaddr', re-format it
            if "macaddr" in n2["user"]:
                val = n2["user"]["macaddr"]
                # decode the base64 value
                addr = convert_mac_addr(val)
                n2["user"]["macaddr"] = addr

            # use id as dictionary key for correct json format in list of nodes
            nodeid = n2["user"]["id"]
            nodes[nodeid] = n2

    data["nodes"] = nodes 
    return data


data = createInfoJson(node)
print(json.dumps(data))

