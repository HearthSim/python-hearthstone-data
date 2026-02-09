import os
import sys

if sys.version_info < (3, 9):
	import pkg_resources

	__version__ = pkg_resources.require("hearthstone_data")[0].version

	def get_bountydefs_path():
		return pkg_resources.resource_filename("hearthstone_data", "BountyDefs.xml")

	def get_carddefs_path():
		return pkg_resources.resource_filename("hearthstone_data", "CardDefs.xml")

	def get_mercenarydefs_path():
		return pkg_resources.resource_filename("hearthstone_data", "MercenaryDefs.xml")

	def get_strings_file(locale="enUS", filename="GLOBAL.txt"):
		path = os.path.join("Strings", locale, filename)

		return pkg_resources.resource_filename("hearthstone_data", path)

else:
	from importlib.metadata import version
	from importlib.resources import files

	__version__ = version("hearthstone_data")

	def get_bountydefs_path():
		return files("hearthstone_data").joinpath("BountyDefs.xml")

	def get_carddefs_path():
		return files("hearthstone_data").joinpath("CardDefs.xml")

	def get_mercenarydefs_path():
		return files("hearthstone_data").joinpath("MercenaryDefs.xml")

	def get_strings_file(locale="enUS", filename="GLOBAL.txt"):
		path = os.path.join("Strings", locale, filename)

		return files("hearthstone_data").joinpath(path)
