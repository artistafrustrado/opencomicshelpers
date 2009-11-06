!/bin/bash

VERSION=$2
PACK=$1

PACK=$(echo $PACK | sed -r 's#/##g')

cp -fr $PACK $PACK-$VERSION
tar -zcvf $PACK-$VERSION.tar.gz $PACK-$VERSION/

cd $PACK-$VERSION
sed -r "s#0.0.1#$VERSION#g" -i debian/changelog
sed -r "s#0.0.1#$VERSION#g" -i debian/files
find . -iname ".svn" -exec rm -fr {} \;


dpkg-buildpackage -rfakeroot
