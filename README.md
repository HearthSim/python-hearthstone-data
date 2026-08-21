# hearthstone-data

[![PyPI](https://img.shields.io/pypi/v/hearthstone_data)](https://pypi.org/project/hearthstone_data/)
[![Trigger release](https://img.shields.io/badge/release-trigger-success)](https://github.com/HearthSim/python-hearthstone-data/actions/workflows/release.yml)

This repository is used to package Hearthstone's card data as the [hearthstone_data package](https://pypi.org/project/hearthstone_data/) on PyPI.

`CardDefs.xml`, `BountyDefs.xml` and `MercenaryDefs.xml` are sourced from [api.hearthstonejson.com](https://api.hearthstonejson.com/v1/latest/). The strings files are not published there and still come from [hsdata](https://github.com/HearthSim/hsdata).

The build script will automatically fetch the latest data and generate a new version of this package with the appropriate build number. No changes or commits to this repository are necessary as part of the release process.

## Automated Release

To trigger an automated release via GitHub actions, [open this page](https://github.com/HearthSim/python-hearthstone-data/actions/workflows/release.yml) and click "Run workflow".

## Manual Release

Prerequisites:
- `xmllint` (e.g. Debian/Ubuntu: `libxml2-utils`)
- `curl` and `git`

Ensure that `wheel` is installed in your Python environment or virtualenv.

Then, run the following:
```
$ git clean -xfd
$ ./bootstrap.sh
$ python setup.py sdist bdist_wheel upload --sign
```
