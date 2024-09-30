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
    # print(f"seq_try {path}")
    for server in servers:
        # print(f"  → {server}")
        try:
            d = requests.get(
                f"https://{server}{path}", timeout=10, headers=headers
            ).json()
            if 'err_msg' in d:
                continue
            # print(f"  success")
            return d
        except Exception:
            # print(f"Failed to fetch {server}{path}")
            pass


def download_api(tool_id):
    # print(f"Downloading {tool_id}")
    if tool_id.count("/") > 4:
        tool_id_without_version = "/".join(tool_id.split("/")[0:-1])
    else:
        tool_id_without_version = tool_id

    # If exactly this tool id was already downloaded, skip
    if os.path.exists("api/tools/" + tool_id):
        # print("Already downloaded")
        return None

    meta = seq_try(f"/api/tools/{tool_id}?io_details=True&link_details=False", SERVERS)
    if meta is None or "name" not in meta:
        # print("Meta is none:", meta)
        return None
    else:
        # make dir
        os.makedirs("api/tools/" + tool_id_without_version, exist_ok=True)
        print(f"Downloaded {tool_id}")
        with open("api/tools/" + tool_id, "w") as handle:
            json.dump(meta, handle)


with open("guid-rev.json") as f:
    guid_rev = json.load(f)
    tool_ids = set(guid_rev.keys())
print(f"Found {len(tool_ids)} tools")


# Existing 
import glob
existing_tool_ids = glob.glob("api/**/*", recursive=True)
existing_tool_ids = [x for x in existing_tool_ids if os.path.isfile(x)]
existing_tool_ids = set([x[len("api/tools/"):] for x in existing_tool_ids])

tool_ids = list(tool_ids - existing_tool_ids)
print(f"Reduced to {len(tool_ids)} tools")
thread_map(download_api, tool_ids, max_workers=1)
