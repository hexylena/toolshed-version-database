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

for server in SERVERS:
    # curl https://{server}/api/tools?in_panel=False | jq .[].id
    data = requests.get(f"https://{server}/api/tools?in_panel=False").json()
    for tool in data:
        tool_id = tool["id"]
        if tool_id.count("/") > 4:
            continue

        if os.path.exists(f"api/tools/{tool_id}"):
            continue

        print(f"Downloading {tool_id}")
        print(
            f"https://{server}/api/tools/{tool_id}?io_details=True&link_details=False"
        )
        meta = requests.get(
            f"https://{server}/api/tools/{tool_id}?io_details=True&link_details=False"
        ).json()
        if "name" not in meta:
            print(f"Skipping {tool_id}")
            continue
        with open(f"api/tools/{tool_id}", "w") as f:
            json.dump(meta, f, indent=2)
