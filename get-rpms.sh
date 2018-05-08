#!/bin/sh

VERSION="$1"
if [ -z ${VERSION} ]; then
  if [ -d "SPECS" ]; then
    VERSION=$(grep "Version:" SPECS/flash-player-plugin.spec | cut -f2)
  else
    echo "Please give a version number as argument, or run from the parent of the SPECS folder to parse the Version tag."
    exit 0
  fi
fi

MIRROR1="http://fpdownload.adobe.com/get/flashplayer/pdc/${VERSION}"
MIRROR2="http://fpdownload.adobe.com/get/flashplayer/current/licensing/linux"
MIRROR3="http://linuxdownload.adobe.com/linux"

DL_DIR="/tmp/flash-player-plugin-${VERSION}-adobe-rpms"
rm -rf ${DL_DIR} && mkdir -p ${DL_DIR}

# Download i386 RPMs

FILENAME_I386="flash-player-ppapi-${VERSION}-release.i386.rpm"

wget -P ${DL_DIR}/url1 ${MIRROR1}/${FILENAME_I386}
wget -P ${DL_DIR}/url2 ${MIRROR2}/${FILENAME_I386}
wget -P ${DL_DIR}/url3 ${MIRROR3}/i386/${FILENAME_I386}

# Download x86_64 RPMs

FILENAME_X86_64="flash-player-ppapi-${VERSION}-release.x86_64.rpm"

wget -P ${DL_DIR}/url1 ${MIRROR1}/${FILENAME_X86_64}
wget -P ${DL_DIR}/url2 ${MIRROR2}/${FILENAME_X86_64}
wget -P ${DL_DIR}/url3 ${MIRROR3}/x86_64/${FILENAME_X86_64}

# Compute sha256sums needed in spec file

for file in ${FILENAME_I386} ${FILENAME_X86_64}; do
  for dir in url1 url2 url3; do
    RPMFILE="${DL_DIR}/${dir}/${file}"
    SHA256SUM=$(sha256sum ${RPMFILE} | cut -f1 -d' ')
    SIZE=$(stat --printf="%s" ${RPMFILE})
    echo -e "${dir}/${file}:\n${SHA256SUM}:${SIZE}\n"
  done
done
