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
from nova.network import model
CONF = cfg.CONF

LOG = logging.getLogger(__name__)

# original monkey patched functions references
get_neutron_network = None

def decorator(name, function):
    """This function must be used with the monkey_patch_modules option in
    nova.conf
    Example::
       monkey_patch=true
       monkey_patch_modules=nova.virt.vmwareapi.vif:\
                 esxi_mitaka_nuage_nova.nova.virt.vmwareapi.vif.decorator
    """
    global get_neutron_network

    if name == 'nova.virt.vmwareapi.vif._get_neutron_network':
        get_neutron_network = function
        return _get_neutron_network
    else:
        return function


def _get_neutron_network(session, cluster, vif):
    if vif['type'] == model.VIF_TYPE_OVS:
        _check_ovs_supported_version(session)
        #import pdb; pdb.set_trace()
        # Check if this is the NSX-MH plugin is used
        if CONF.vmware.integration_bridge:
            net_id = CONF.vmware.integration_bridge
            use_external_id = False
            network_type = 'opaque'
        else:
           network_id = vif['network']['bridge']
        network_ref = network_util.get_network_with_the_name(
                session, network_id, cluster)
        if not network_ref:
            raise exception.NetworkNotFoundForBridge(bridge=network_id)

    elif vif['type'] == model.VIF_TYPE_DVS:
        network_id = vif['network']['bridge']
        network_ref = network_util.get_network_with_the_name(
                session, network_id, cluster)
        if not network_ref:
            raise exception.NetworkNotFoundForBridge(bridge=network_id)
    else:
        reason = _('vif type %s not supported') % vif['type']
        raise exception.InvalidInput(reason=reason)
    return network_ref

