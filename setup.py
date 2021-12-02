#!/usr/bin/env python

import os
import sys
from setuptools import setup


DEFAULT_RELEASE = "1"


def get_version():
	basedir = os.path.abspath(os.path.dirname(__file__))
	build_path = os.path.join(basedir, "hearthstone_data", "BUILD")

	if not os.path.exists(build_path):
		sys.stderr.write("Cannot file BUILD file. Generate with ./bootstrap.sh.\n")
		exit(1)

	with open(build_path, "r") as f:
		hearthstone_build = f.read().strip()

	assert hearthstone_build
	assert hearthstone_build.isdigit()

	release = os.environ.get("PKGREL", DEFAULT_RELEASE)
	assert release.isdigit()

	return ".".join([hearthstone_build, release])


setup(
	version=get_version(),
	package_data={"": ["BountyDefs.xml", "CardDefs.xml", "MercenaryDefs.xml", "Strings/*/*.txt", "BUILD"]},
)
