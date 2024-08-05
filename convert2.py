#!/usr/bin/env python3
import json
import argparse

with open("tool-meta.tsv", "r") as handle:
    data = [x.strip("\n").split("\t") for x in handle]

tool_meta = {}

for guid, name, description, edam_operations, edam_topics in data:
    tool_meta[guid] = {
        "name": name,
        "desc": description,
        "edam_operations": edam_operations.split(","),
        "edam_topics": edam_topics.split(","),
    }

with open("tool-meta.json", "w") as handle:
    json.dump(tool_meta, handle)
