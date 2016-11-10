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


from oslo_config import cfg
from oslo_log import log as logging

CONF = cfg.CONF

LOG = logging.getLogger(__name__)

# original monkey patched functions references
_get_domain = None

def decorator(name, function):
    """This function must be used with the monkey_patch_modules option in
    nova.conf
    Example::
       monkey_patch=true
       monkey_patch_modules=nova.virt.libvirt.host:\
                 nuage_nova.nova.virt.libvirt.host.decorator
    """
    global _get_domain

    if name == 'nova.virt.libvirt.host.Host.get_domain':
        _get_domain = function
        return get_domain
    else:
        return function


def get_domain(self, instance):
    """Retrieve libvirt domain object for an instance.

    :param instance: an nova.objects.Instance object

    Attempt to lookup the libvirt domain objects
    corresponding to the Nova instance, based on
    its name. If not found it will raise an
    exception.InstanceNotFound exception. On other
    errors, it will raise a exception.NovaException
    exception.

    :returns: a libvirt.Domain object
    """
    return self._get_domain_by_name(instance.display_name)
