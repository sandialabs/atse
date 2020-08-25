#!/bin/bash
#
#
if ! test -f ovispyversion; then
	echo "download.sh: must be from the ldms_434/SOURCES directory"
	exit 1
fi
export PYVERSION=$(cat ./ovispyversion)
export COLLVERSION=$(cat ./ovisversion)
SCL=sandia-nosos-ovis_${COLLVERSION}
packing=v4.atse.opt.nosos.unstable
top=$(pwd)
PART=LDMS
ovis_branch=munge_genders_v4
NetworkRequires=github.com
OVISREPO=https://github.com/baallan/ovis.git

if test -n "$MODULEPATH"; then
	module purge
fi
/bin/rm -rf $PART
if ! git clone $OVISREPO $PART; then
	echo cannot checkout ovis.
	exit 1
fi

cd $PART
if ! git checkout $ovis_branch; then
	echo cannot checkout ovis branch $ovis_branch.
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
PACKAGE=ovis-ldms
# Find SHA of latest checkin someone tagged
set -x
COMMIT_ID="$(git log -1 --pretty="%H")"
BASE_COMMIT_ID="$(git rev-parse $ovis_branch)"
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

# Untar archive
echo "Untarring archive"
tar xf $TARGET && \
(cd ${PACKAGE}-${VERSION} && \
./autogen.sh)
if ! test -f ${PACKAGE}-${VERSION}/configure; then
	echo "unable to generate $PART build files"
	exit 1
fi

# Tar back up excluding unwanted files and dirs
echo "tarring archive with excludes from "
echo "$REPO_DIR/util/tar-excludes.txt"
TAR_OPTS="-X $REPO_DIR/util/tar-excludes.txt"
tar czf $TARGET.gz $TAR_OPTS ${PACKAGE}-${VERSION}

echo "Relocating cruft"
rm -rf old
mkdir old
mv -f ${PACKAGE}-${VERSION} $TARGET old

tar zxf $TARGET.gz && \
/bin/rm $TARGET.gz && \
cd ${PACKAGE}-${VERSION} && \
echo "================ configure for $packing rpms =============" && \
./configure CC=gcc CXX=g++ $allconfig && \
echo "============================= make $packing rpms =============" && \
make dist-gzip
cp ovis-ldms-4.3.4.tar.gz $top/
cd $top
sha256sum ovis-ldms-4.3.4.tar.gz > ovis-ldms-4.3.4.tar.gz.sha256

