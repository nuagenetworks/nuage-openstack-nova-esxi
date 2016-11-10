# Copyright 2016 Alcatel-Lucent USA Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import os
from oslo_config import cfg
from oslo_log import log as logging
from oslo_utils import strutils
from nova.virt.libvirt import utils as libvirt_utils

CONF = cfg.CONF

LOG = logging.getLogger(__name__)

# original monkey patched functions references
get_guest_xml = None

def decorator(name, function):
    """This function must be used with the monkey_patch_modules option in
    nova.conf
    Example::
       monkey_patch=true
       monkey_patch_modules=nova.virt.libvirt.driver:\
                 nuage_nova.nova.virt.libvirt.driver.decorator
    """
    global get_guest_xml

    if name == 'nova.virt.libvirt.driver.LibvirtDriver._get_guest_xml':
        get_guest_xml = function
        return _get_guest_xml
    else:
        return function

def _get_guest_xml(self, context, instance, network_info, disk_info,
                   image_meta, rescue=None,
                   block_device_info=None, write_to_disk=False):
    # NOTE(danms): Stringifying a NetworkInfo will take a lock. Do
    # this ahead of time so that we don't acquire it while also
    # holding the logging lock.
    network_info_str = str(network_info)
    msg = ('Start _get_guest_xml '
           'network_info=%(network_info)s '
           'disk_info=%(disk_info)s '
           'image_meta=%(image_meta)s rescue=%(rescue)s '
           'block_device_info=%(block_device_info)s' %
           {'network_info': network_info_str, 'disk_info': disk_info,
            'image_meta': image_meta, 'rescue': rescue,
            'block_device_info': block_device_info})
    # NOTE(mriedem): block_device_info can contain auth_password so we
    # need to sanitize the password in the message.
    LOG.debug(strutils.mask_password(msg), instance=instance)
    conf = self._get_guest_config(instance, network_info, image_meta,
                                  disk_info, rescue, block_device_info,
                                  context)
    conf.name = conf.metadata[0].name
    xml = conf.to_xml()

    if write_to_disk:
        instance_dir = libvirt_utils.get_instance_path(instance)
        xml_path = os.path.join(instance_dir, 'libvirt.xml')
        libvirt_utils.write_to_file(xml_path, xml)

    LOG.debug('End _get_guest_xml xml=%(xml)s',
              {'xml': xml}, instance=instance)
    return xml
