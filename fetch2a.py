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
    "User-Agent": "tsvdb@1a (https://github.com/hexylena/toolshed-version-database/)",
}


def seq_try(path, servers):
    for server in servers:
        try:
            return requests.get(
                f"https://{server}{path}", timeout=10, headers=headers
            ).json()
        except Exception as e:
            print(e)
            pass


def download_api(tool_id):
    if tool_id.count("/") > 4:
        tool_id_without_version = "/".join(tool_id.split("/")[0:-1])
    else:
        tool_id_without_version = tool_id

    # If exactly this tool id was already downloaded, skip
    if os.path.exists("api/tools/" + tool_id):
        return None

    meta = seq_try(f"/api/tools/{tool_id}?io_details=True&link_details=False", SERVERS)
    if meta is None or "name" not in meta:
        return None
    else:
        # make dir
        os.makedirs("api/tools/" + tool_id_without_version, exist_ok=True)
        with open("api/tools/" + tool_id, "w") as handle:
            json.dump(meta, handle)


with open("guid-rev.json") as f:
    guid_rev = json.load(f)
    tool_ids = set(guid_rev.keys())
print(f"Found {len(tool_ids)} tools")

thread_map(download_api, list(tool_ids), max_workers=10)
