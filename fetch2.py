#!/usr/bin/env python3
import os
import requests
import json
import sys
import time
from tqdm.contrib.concurrent import thread_map

SERVERS = [
    "usegalaxy.eu",
    "usegalaxy.fr",
    "usegalaxy.org",
    "usegalaxy.org.au",
    #
    "usegalaxy.be",
    "usegalaxy.cz",
    "usegalaxy.no",
    "usegalaxy.es",
    # The rest of the public servers list.
    "cpt.tamu.edu/galaxy-public",
    "galaxy-web.ipk-gatersleben.de",
    "galaxy.bio.di.uminho.pt",
    "galaxy.hyphy.org",
    "galaxy.mesocentre.uca.fr",
    "galaxy.pasteur.fr",
    "galaxytrakr.org",
    "hyperbrowser.uio.no/coloc-stats",
    "iris.angers.inra.fr/galaxypub-cfbp",
    "mississippi.sorbonne-universite.fr",
    "neo.engr.uconn.edu",
    "palfinder.ls.manchester.ac.uk",
    "vm-chemflow-francegrille.eu",
    "www.immportgalaxy.org",
]


def fetch_name(tool_id):
    if not os.path.exists(f"api/tools/{tool_id}"):
        return None

    with open(f"api/tools/{tool_id}", 'r') as handle:
        meta = json.load(handle)

    biotools_xrefs = [x['value'] for x in meta.get('xrefs', []) if x['reftype'] == 'bio.tools']

    return [
        tool_id,
        meta["name"],
        meta["description"],
        ",".join(meta["edam_operations"]),
        ",".join(meta["edam_topics"]),
        biotools_xrefs[0] if len(biotools_xrefs) > 0 else "",
    ]




with open("guid-rev.json") as f:
    guid_rev = json.load(f)
    tool_ids = set(guid_rev.keys())
print(f"Found {len(tool_ids)} tools")

if os.path.exists("tool-meta.tsv"):
    with open("tool-meta.tsv") as f:
        existing = set([line.split("\t")[0] for line in f])
        tool_ids = tool_ids - existing
print(f"{len(tool_ids)} tools are missing metadata")

r = thread_map(fetch_name, list(tool_ids), max_workers=10)
with open("tool-meta.tsv", "a") as f:
    results = [x for x in list(r) if x is not None]
    print(f"Fetched {len(results)} updates")
    for repo_result in results:
        f.write("\t".join(repo_result) + "\n")

with open("tool-meta.tsv", "r") as handle:
    data = [x.strip("\n").split("\t") for x in handle]

tool_meta = {}

for guid, name, description, edam_operations, edam_topics, bio_tools in data:
    tool_meta[guid] = {
        "name": name,
        "desc": description,
        "edam_operations": edam_operations.split(","),
        "edam_topics": edam_topics.split(","),
        "bio.tools": bio_tools,
    }

with open("tool-meta.json", "w") as handle:
    json.dump(tool_meta, handle)
