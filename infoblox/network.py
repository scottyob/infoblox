"""
Base Network Object

"""
import logging

from infoblox import exceptions
from infoblox import mapping
from infoblox.mappingDb import MappingDb

LOGGER = logging.getLogger(__name__)

class Network(MappingDb):
    """This object impliments the DHCP Network Object.

    Example::

        session = infblox.Session(inblox_host,
                                  infoblox_user,
                                  infoblox_password)
        network = infoblox.Network(session, address='1.2.3.0/24')
    """

    authority = None # Bool
    auto_create_reversezone = None #   Bool
    bootfile = None #  String
    bootserver = None #    String
    comment = None #   String
    ddns_domainname = None #   String
    ddns_generate_hostname = None #    Bool
    ddns_server_always_updates = None #    Bool
    ddns_ttl = None #  Unsigned
    ddns_update_fixed_addresses = None #   Bool
    ddns_use_option81 = None # Bool
    deny_bootp = None #    Bool
    disable = None #   Bool
    email_list = None #    [String]
    enable_ddns = None #   Bool
    enable_dhcp_thresholds = None #    Bool
    enable_email_warnings = None # Bool
    enable_ifmap_publishing = None #   Bool
    enable_snmp_warnings = None #  Bool
    extattrs = None #  Extattr
    high_water_mark = None #   Unsigned
    high_water_mark_reset = None # Unsigned
    ignore_dhcp_option_list_request = None #   Bool
    ipv4addr = None #  String
    lease_scavenge_time = None #   Integer
    low_water_mark = None #    Unsigned
    low_water_mark_reset = None #  Unsigned
    members = None #   [struct]
    netmask = None #   Unsigned
    network = None #   String
    network_container = None # String
    network_view = None #  String
    nextserver = None #    String
    options = None #   [struct]
    pxe_lease_time = None #    Unsigned
    recycle_leases = None #    Bool
    template = None #  String
    update_dns_on_lease_renewal = None #   Bool
    use_authority = None # Bool
    use_bootfile = None #  Bool
    use_bootserver = None #    Bool
    use_ddns_domainname = None #   Bool
    use_ddns_generate_hostname = None #    Bool
    use_ddns_ttl = None #  Bool
    use_ddns_update_fixed_addresses = None #   Bool
    use_ddns_use_option81 = None # Bool
    use_deny_bootp = None #    Bool
    use_email_list = None #    Bool
    use_enable_ddns = None #   Bool
    use_enable_dhcp_thresholds = None #    Bool
    use_enable_ifmap_publishing = None #   Bool
    use_ignore_dhcp_option_list_request = None #   Bool
    use_lease_scavenge_time = None #   Bool
    use_nextserver = None #    Bool
    use_options = None #   Bool
    use_recycle_leases = None #    Bool
    use_update_dns_on_lease_renewal = None #   Bool
    use_zone_associations = None # Bool
    zone_associations = None # [struct]

    _return_ignore = ['view', 'auto_create_reversezone', 'template', 'name']
    _search_by = ['comment', 'ipv4addr','network', 'network_container', 'network_view']
    # _search_by = ['network']
    _supports = ['fetch', 'put', 'save']
    _wapi_type = 'network'

    #Probably best to take the following out and abstract it??
    _save_ignore = []
#    _path = 

    def __init__(self, session, reference_id=None, **kwargs):
        """Create a new instance of a Network object.  If a reference_id or valid
        search criteria are passed in, the object will attempt to load the
        values for the Network from the Infoblox device.

        Valid search criteria: comment, extattrs, ipv4addr, network, network_container, network_view

        :param infobox.Session session: The established session object
        :param str reference_id: The Infoblox reference id for the host
        :param str host: The host's FQDN
        :param dict kwargs: Optional keyword arguments
        
        """

        super(Network, self).__init__(session, reference_id, **kwargs)
 
#        if self._ref or self._search_values:
#            self.fetch()
#
