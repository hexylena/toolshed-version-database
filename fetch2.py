#!/usr/bin/env python3
import glob
import os
import requests
import json
from tqdm.contrib.concurrent import thread_map


def map_biotools_xref(b):
    if b == 'hmmsearch':
        return 'hmmer3'
    elif b == 'jbrowse2':
        return 'jbrowse_2'
    elif b == 'resqc':
        return 'rseqc'
    elif b == 'humann3':
        return 'humann'
    elif b == 'mummer4':
        return 'mummer'
    elif b == 'alphafold_2.0':
        return 'alphafold_2'
    elif b == 'encylopeDIA':
        return 'EncyclopeDIA'
    else:
        return b



def fetch_name(tool_id):
    if not os.path.exists(f"api/tools/{tool_id}"):
        return None

    with open(f"api/tools/{tool_id}", 'r') as handle:
        try:
            meta = json.load(handle)
        except:
            print(f"Could not load {tool_id}")
            raise Exception()

    biotools_xrefs = [x['value'] for x in meta.get('xrefs', []) if x.get('reftype') == 'bio.tools']
    biotools_name = ""
    biotools_xref = ""
    if len(biotools_xrefs) > 0:
        biotools_xref = biotools_xrefs[0]
        biotools_xref = biotools_xref.split(', ')[0]
        biotools_xref = biotools_xref.split(' ')[0]
        biotools_xref = map_biotools_xref(biotools_xref)

        if os.path.exists(f"api/biotools/{biotools_xref}"):
            with open(f"api/biotools/{biotools_xref}", 'r') as handle:
                try:
                    bmeta = json.load(handle)
                    biotools_name = bmeta.get('name', "")
                    if biotools_name == "":
                        print(f"Could not load t={tool_id} b={biotools_xref}")
                except:
                    print(f"Could not decode t={tool_id} b={biotools_xref}")
                    pass
        else:
            req = requests.get(f"https://bio.tools/api/tool/{biotools_xref}", headers={"Accept": "application/json"}, timeout=10)
            try:
                data = req.json()
            except:
                raise Exception(f"Could not load t={tool_id} b={biotools_xref} {req} {req.text}")
            with open(f"api/biotools/{biotools_xref}", 'w') as handle:
                handle.write(req.text)

            if 'name' not in data:
                print(data)
            else:
                biotools_name = data['name']

    return [
        tool_id,
        meta["name"],
        meta["description"],
        ",".join(meta["edam_operations"]),
        ",".join(meta["edam_topics"]),
        biotools_xref,
        biotools_name,
        meta.get('xrefs', [])
    ]


tool_ids = glob.glob("api/**/*", recursive=True)
tool_ids = [x for x in tool_ids if os.path.isfile(x)]
tool_ids = [x[len("api/tools/"):] for x in tool_ids]


r = thread_map(fetch_name, list(tool_ids), max_workers=10)
tool_meta = {}
tool_meta_v2 = {}

with open("tool-meta.tsv", "w") as f:
    results = [x for x in list(r) if x is not None]
    print(f"Fetched {len(results)} updates")
    for (guid, name, description, edam_operations, edam_topics, biotools_id, biotools_name, xrefs) in results:

        f.write("\t".join((guid, name, description, edam_operations, edam_topics, biotools_id, biotools_name)) + "\n")

        tool_meta[guid] = {
            "name": name,
            "desc": description,
            "edam_operations": [x for x in edam_operations.split(",") if x != ""],
            "edam_topics": [x for x in edam_topics.split(",") if x != ""],
            "bio.tools": biotools_id,
            "bio.tools_name": biotools_name,
            # "xrefs": xrefs,
        }

        tool_meta_v2[guid] = {
            "name": name,
            "desc": description,
            "edam_operations": [x for x in edam_operations.split(",") if x != ""],
            "edam_topics": [x for x in edam_topics.split(",") if x != ""],
            "xrefs": xrefs,
        }

with open("tool-meta.json", "w") as handle:
    json.dump(tool_meta, handle)

with open("tool-meta-2.json", "w") as handle:
    json.dump(tool_meta_v2, handle)

import subprocess
subprocess.check_call(['bash', '-c', 'cat tool-meta.json | jq -c > tmp'])
subprocess.check_call(['mv', 'tmp', 'tool-meta.json'])

subprocess.check_call(['bash', '-c', 'cat tool-meta-2.json | jq -c > tmp'])
subprocess.check_call(['mv', 'tmp', 'tool-meta-2.json'])
