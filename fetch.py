#!/usr/bin/env python3
import sys
import time
import bioblend
from bioblend import toolshed
from tqdm.contrib.concurrent import thread_map


def fetch_versions(repo):
    ret = []
    revs = []
    try:
        revs = ts.repositories.get_ordered_installable_revisions(repo['name'], repo['owner']):
    except bioblend.ConnectionError:
        time.sleep(10)
        try:
            revs = ts.repositories.get_ordered_installable_revisions(repo['name'], repo['owner']):
        except bioblend.ConnectionError:
            sys.stderr.write(f"Could not get revision list for {repo['name']} {repo['owner']}\n")
            return ret

    for rev in revs:
        try:
            e = ts.repositories.get_repository_revision_install_info(repo['name'], repo['owner'], rev)
        except bioblend.ConnectionError:
            time.sleep(10)
            try:
                e = ts.repositories.get_repository_revision_install_info(repo['name'], repo['owner'], rev)
            except bioblend.ConnectionError:
                sys.stderr.write(f"Could not fetch the results of {repo['name']} {repo['owner']} {rev}\n")
                continue

        if 'valid_tools' not in e[1]:
            res = [
                repo['name'],
                repo['owner'],
                rev,
                'invalid',
                'invalid',
                'invalid',
            ]
            ret.append(res)
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
            ret.append(res)
    return ret



ts = toolshed.ToolShedInstance(url='https://toolshed.g2.bx.psu.edu')
repos = ts.repositories.get_repositories()

r = thread_map(fetch_versions, repos, max_workers=10)
for repo_result in r:
    for rev_result in repo_result:
        print("\t".join(rev_result))
