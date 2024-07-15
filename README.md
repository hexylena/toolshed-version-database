# toolshed-version-database

I've needed since years something to map tool IDs + versions back to which repository revision I need to install. I understand the toolshed is miserable to work with, so, fair, but, I still need this so we're just going to scrape it.

## Data

File | Purpose
--- | ---
[guid-rev.json](guid-rev.json) | Map a tool guid (e.g `toolshed.g2.bx.psu.edu/repos/iuc/circos/circos/0.69.8+galaxy1` to the triple of owner/name/rev, like `("iuc", "circos", "014a21767ac4")`.
[tool-version-database.tsv](tool-version-database.tsv) | Full table of (repo name, repo owner, repo revision, tool name, tool guid, version) (yes guid is a bit redundant.)
[tool-meta.tsv](tool-meta.tsv) | Table of (guid, name, description, edam operations, edam topics)
[tool-meta.json](tool-meta.json) | Same but json
api/tools/* | The result of `/api/tools/*?io_details=True&link_details=False` for the first server that would answer. Will be replaced by https://github.com/galaxyproject/galaxy/pull/18524

## LICENSE

AGPL-3.0
