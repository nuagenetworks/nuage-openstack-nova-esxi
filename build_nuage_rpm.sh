#!/bin/bash
# 
# Name:
#
set -e

################# Handle build metadata #######################################
# we handle nightly builds only for now
OVS_BUILD_NUMBER=$(echo $BUILD_NAME | sed "s/^.*-\(.*\)$/\1/")



# create SOURCE0 for spec file
git archive --format=tar --prefix=nuage-nova-esxi-4.0.7/ HEAD | gzip > rhel/SOURCES/nuage-nova-esxi-4.0.7.tar.gz

# build rpm's
rpmbuild -ba --define "_topdir `pwd`/rhel" --define "build_number ${OVS_BUILD_NUMBER}" rhel/nuage-nova-esxi.spec
