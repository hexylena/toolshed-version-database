#!/usr/bin/env python3
import sys
# this is how to get tool info from the toolshed
import bioblend
from bioblend import toolshed
import tqdm
toolshed_name = 'toolshed.g2.bx.psu.edu'
toolshed_url = f'https://{toolshed_name}'

processed = []
with open('tool-version-database.tsv', 'r') as handle:
    data = [x.split('\t') for x in handle.readlines()]
    for x in data:
        processed.append(
            (x[0], x[1])
        )

# Dunno if that last one is fully processed, all revisions of it.
if len(processed) > 0:
    last_processed = processed[-1]
    processed = list(set(processed))
    processed.remove(last_processed)


ts = toolshed.ToolShedInstance(url=toolshed_url)

for repo in tqdm.tqdm(ts.repositories.get_repositories()):
    key = (repo['name'], repo['owner'])
    if key in processed:
        continue

    for rev in ts.repositories.get_ordered_installable_revisions(repo['name'], repo['owner']):
        try:
            e = ts.repositories.get_repository_revision_install_info(repo['name'], repo['owner'], rev)
        except bioblend.ConnectionError:
            sys.stderr.write(f"Could not fetch the results of {repo['name']} {repo['owner']} {rev}\n")

        if 'valid_tools' not in e[1]:
            res = [
                repo['name'],
                repo['owner'],
                rev,
                'invalid',
                'invalid',
                'invalid',
            ]
            print('\t'.join(res))

            continue

        for valid_tool in e[1]['valid_tools']:
            res = [
                repo['name'],
                repo['owner'],
                rev,
                valid_tool['id'],
                valid_tool['guid'],
                valid_tool['version'],
            ]
            print('\t'.join(res))
