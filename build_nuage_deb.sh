#!/bin/bash
#
# Name:
#
set -e

################# Handle build metadata #######################################
# we handle nightly builds only for now
OVS_BUILD_NUMBER=$(echo $BUILD_NAME | sed "s/^.*-\(.*\)$/\1/")


DEBEMAIL="Nuage Networks <info@nuagenetworks.net>" dch -b --newversion \
            4.2.4-${OVS_BUILD_NUMBER} "Jenkins build" --distribution $(lsb_release --codename --short)


###
# build packages
#debuild -d -i -us -uc -ba
debuild -d -i -us -uc -b -kinfo@nuagenetworks.net
