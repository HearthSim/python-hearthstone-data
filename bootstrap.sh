#!/bin/bash

BASEDIR="$(dirname "$0")"
HSDATA_URL="https://github.com/HearthSim/hsdata.git"
HSDATA_DIR="$BASEDIR/build/hs-data"
PACKAGE_DIR="$BASEDIR/hearthstone_data"
BUILD="$(xmllint --xpath "string(/*/@build)" "$HSDATA_DIR/CardDefs.xml")"

command -v xmllint &>/dev/null || {
	>&2 echo "ERROR: xmllint is required to bootstrap this project."
	exit 1
}

command -v git &>/dev/null || {
	>&2 echo "ERROR: git is required to bootstrap this project."
	exit 1
}

mkdir -p "$BASEDIR/build"

echo "Fetching data files from $HSDATA_URL"
if [[ ! -e "$HSDATA_DIR" ]]; then
	git clone --depth=1 "$HSDATA_URL" "$HSDATA_DIR"
else
	git -C "$HSDATA_DIR" fetch &&
	git -C "$HSDATA_DIR" reset --hard origin/master
fi

cp "$HSDATA_DIR/BountyDefs.xml" "$PACKAGE_DIR/BountyDefs.xml"
cp "$HSDATA_DIR/CardDefs.xml" "$PACKAGE_DIR/CardDefs.xml"
cp "$HSDATA_DIR/MercenaryDefs.xml" "$PACKAGE_DIR/MercenaryDefs.xml"
rm -rf "$BASEDIR/hearthstone_data/Strings"
cp -rf "$HSDATA_DIR/Strings" -t "$PACKAGE_DIR"
rm "$PACKAGE_DIR/Strings"/*/CREDITS_*.txt
echo "$BUILD" > "$PACKAGE_DIR/BUILD"
