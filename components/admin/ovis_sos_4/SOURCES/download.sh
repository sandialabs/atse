#!/bin/bash
#
#
if test -n "$MODULEPATH"; then
	module purge
fi
export https_proxy=wwwproxy.sandia.gov:80
if ! test -f ovispyversion; then
	echo "download.sh: must be from the ovis_sos_4/SOURCES directory"
	exit 1
fi
export PYVERSION=$(cat ./ovispyversion)
export COLLVERSION=$(cat ./ovisversion)
top=$(pwd)
sos_branch=SOS-4
NetworkRequires=github.com
SOSREPO=https://github.com/ovis-hpc/sos.git
PART=sos-4
if ! git clone $SOSREPO $PART; then
	echo cannot checkout sos
	exit 1
fi

cd $PART
if ! git checkout $sos_branch; then
	echo cannot checkout sos branch $sos_branch.
	exit 1
fi
cd ..

cd $PART
patches=""
for i in $patches; do
	# patch -p1 < ../patches/$i
	git apply ../patches/$i
	git commit -a -m "add $packing distribution patches: $i"
done
newfiles=""
if test -n "$newfiles"; then
	git add $newfiles
	git commit -a -m "add $packing distribution files: $newfilest"
fi

VERSION=4.3.4
PACKAGE=ovis-sos
# Find SHA of latest checkin someone tagged
set -x
COMMIT_ID="$(git log -1 --pretty="%H")"
BASE_COMMIT_ID="$(git rev-parse $sos_branch)"
# Get most recent tag id for this branch
#TAG_ID="$(git describe --tags --abbrev=0)"
set +x
TARGET=${PACKAGE}-${VERSION}.tar
REPO_DIR=`pwd`
OUTPUT_DIR=`pwd`/Tars
# Create output dir
mkdir -p $OUTPUT_DIR
# populate outdir inputs
git archive --prefix=${PACKAGE=}-${VERSION}/ $COMMIT_ID --format=tar --output=${OUTPUT_DIR}/$TARGET
cd ..

sleep 0.1

cd $OUTPUT_DIR

tar xf $TARGET && \
/bin/rm $TARGET && \
cd ${PACKAGE}-${VERSION} && \
./autogen.sh && \
./configure --disable-python CC=gcc CXX=g++ && \
make dist-gzip
cp sosdb-4.3.4.tar.gz $top/
cd $top
sha256sum sosdb-4.3.4.tar.gz > sosdb-4.3.4.tar.gz.sha256

