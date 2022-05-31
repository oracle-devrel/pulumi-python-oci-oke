from resources.oke import oke
from resources.network import network
from pulumi import Config

""" Load common pulumi config """
config = Config()
""" VCN Creation """
vcn = network().create_vcn(config)

""" Service Gateway for OKE """
service_gateway = network().create_service_gateway(config,vcn)
""" Nat gateway for OKE  """
nat_gateway = network().create_natgateway(config,vcn)
""" Internget gateway for OKE  """
internet_gateway = network().create_internet_gateway(config,vcn)

""" Security list for OKE nodes """
node_security_list = network().create_node_securitylist(config,vcn)
""" Security list for OKE svclb"""
svclb_security_list = network().create_svclb_securitylist(config,vcn)
""" Security list for OKE API endpoint"""
apiendpoint_security_list = network().create_apiendpoint_securitylist(config,vcn)

""" Route table for OKE Node """
oke_node_route_table=network().create_node_routetable(config,vcn,service_gateway,nat_gateway)
""" Route table for oke svclb"""
oke_svclb_route_table=network().create_svclb_routetable(config,vcn,internet_gateway)

""" Subnet for OKE node """
node_subnet = network().create_node_subnet(config,vcn,oke_node_route_table,node_security_list)
""" Subnet for OKE svclb"""
lb_subnet = network().create_lb_subnet(config,vcn,oke_svclb_route_table,svclb_security_list)
""" Subnet for OKE endpoint  """
apiendpoint_subnet = network().create_apiendpoint_subnet(config,vcn,oke_svclb_route_table,apiendpoint_security_list)

"""Creation of OKE Cluster"""
oke_cluster = oke().create_cluster(config,vcn,apiendpoint_subnet,lb_subnet)
"""Creation of OKE node pool"""
oke_nodepool = oke().create_nodepool(config,oke_cluster,node_subnet)
