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

headers = {
    'User-Agent': 'tsvdb@1 (https://github.com/hexylena/toolshed-version-database/)',
}

def seq_try(path, servers):
    for server in servers:
        try:
            return requests.get(f"https://{server}{path}", timeout=10, headers=headers).json()
        except Exception as e:
            print(e)
            pass


def fetch_name(tool_id):
    meta = seq_try(f"/api/tools/{tool_id}?io_details=True&link_details=False", SERVERS)
    if meta is None or "name" not in meta:
        return None
    else:
        return [
            tool_id,
            meta["name"],
            meta["description"],
            ",".join(meta["edam_operations"]),
            ",".join(meta["edam_topics"]),
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
