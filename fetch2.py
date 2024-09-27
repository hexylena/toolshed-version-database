#!/usr/bin/env python3
import glob
import os
import requests
import json
import sys
import time
from tqdm.contrib.concurrent import thread_map


def fetch_name(tool_id):
    if not os.path.exists(f"api/tools/{tool_id}"):
        return None

    with open(f"api/tools/{tool_id}", 'r') as handle:
        try:
            meta = json.load(handle)
        except:
            print(f"Could not load {tool_id}")
            raise Exception()

    biotools_xrefs = [x['value'] for x in meta.get('xrefs', []) if x['reftype'] == 'bio.tools']

    return [
        tool_id,
        meta["name"],
        meta["description"],
        ",".join(meta["edam_operations"]),
        ",".join(meta["edam_topics"]),
        biotools_xrefs[0] if len(biotools_xrefs) > 0 else "",
    ]




tool_ids = glob.glob("api/**/*", recursive=True)
tool_ids = [x for x in tool_ids if os.path.isfile(x)]
tool_ids = [x[len("api/tools/"):] for x in tool_ids]


r = thread_map(fetch_name, list(tool_ids), max_workers=10)
tool_meta = {}

with open("tool-meta.tsv", "w") as f:
    results = [x for x in list(r) if x is not None]
    print(f"Fetched {len(results)} updates")
    for repo_result in results:
        f.write("\t".join(repo_result) + "\n")

        (guid, name, description, edam_operations, edam_topics, bio_tools) = repo_result
        tool_meta[guid] = {
            "name": name,
            "desc": description,
            "edam_operations": edam_operations.split(","),
            "edam_topics": edam_topics.split(","),
            "bio.tools": bio_tools,
        }

with open("tool-meta.json", "w") as handle:
    json.dump(tool_meta, handle)
