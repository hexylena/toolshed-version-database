#!/usr/bin/env python3
import json
import argparse

parser = argparse.ArgumentParser(description='Process database into more useful format(s)')
parser.add_argument('db', type=argparse.FileType('r'))
args = parser.parse_args()

# circos	iuc	ae9994cf526f	circgraph	toolshed.g2.bx.psu.edu/repos/iuc/circos/circgraph/0.9-RC2	0.9-RC2
data = [x.split('\t') for x in args.db.readlines()]
data = [x for x in data if len(x) == 6]

guid_rev = {}

for (name, owner, rev, toolname, guid, version) in data:
    guid_rev[guid] = (owner, name, rev)


with open('guid-rev.json', 'w') as handle:
    json.dump(guid_rev, handle)
