#!/bin/bash

BASEDIR="$(dirname "$0")"
CARDDEFS_URL="https://api.hearthstonejson.com/v1/latest"
HSDATA_URL="https://github.com/HearthSim/hsdata.git"
HSDATA_DIR="$BASEDIR/build/hs-data"
PACKAGE_DIR="$BASEDIR/hearthstone_data"

command -v xmllint &>/dev/null || {
	>&2 echo "ERROR: xmllint is required to bootstrap this project."
	exit 1
}

command -v curl &>/dev/null || {
	>&2 echo "ERROR: curl is required to bootstrap this project."
	exit 1
}

command -v git &>/dev/null || {
	>&2 echo "ERROR: git is required to bootstrap this project."
	exit 1
}

mkdir -p "$BASEDIR/build"

echo "Fetching card data from $CARDDEFS_URL"
for name in BountyDefs.xml CardDefs.xml MercenaryDefs.xml; do
	# bypass the cloudflare cache, which may serve stale defs for up to ~30 minutes after an update
	curl --fail --silent --show-error --compressed \
		-o "$PACKAGE_DIR/$name" "$CARDDEFS_URL/$name?t=$(date +%s)" || exit 1
done

BUILD="$(xmllint --xpath "string(/*/@build)" "$PACKAGE_DIR/CardDefs.xml")"

# the strings files are not published by hearthstonejson, so they still come from hsdata
echo "Fetching strings files from $HSDATA_URL"
if [[ ! -e "$HSDATA_DIR" ]]; then
	git clone --depth=1 --filter=blob:none --no-checkout "$HSDATA_URL" "$HSDATA_DIR" &&
	git -C "$HSDATA_DIR" sparse-checkout set --no-cone "/Strings/" &&
	git -C "$HSDATA_DIR" checkout
else
	git -C "$HSDATA_DIR" fetch &&
	git -C "$HSDATA_DIR" reset --hard origin/master
fi

rm -rf "$PACKAGE_DIR/Strings"
cp -rf "$HSDATA_DIR/Strings" -t "$PACKAGE_DIR"
rm "$PACKAGE_DIR/Strings"/*/CREDITS_*.txt
echo "$BUILD" > "$PACKAGE_DIR/BUILD"
