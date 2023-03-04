# vim: syntax=python

import os
import yaml

from diagrams import Edge
from diagrams import Cluster
from diagrams import Diagram

from diagrams.aws.network import VPC
from diagrams.aws.network import PublicSubnet
from diagrams.aws.network import PrivateSubnet
from diagrams.aws.network import ElbApplicationLoadBalancer
from diagrams.aws.compute import ElasticContainerService
from diagrams.aws.compute import ElasticContainerServiceService

# from diagrams.aws.network.NATGateway
# from diagrams.aws.network.InternetGateway
from diagrams.onprem.client import Users

# LOAD DIAGRAMS SETTINGS
with open("./settings.yml") as yml:
    settings = yaml.safe_load(yml)
gruvbox = settings["styles"]["gruvbox"]
es2 = gruvbox["edges"]["style1"]
ns1 = gruvbox["nodes"]["style1"]
cs3 = gruvbox["clusters"]["style3"]
ds1 = gruvbox["diagrams"]["style1"]

# DIAGRAM CREATION
diagram = {
    "show": False,
    "filename": "diagram",
    "outformat": "png",
    "direction": "LR",  # left - right
    "graph_attr": ds1
}

diagram_title = "\nArchitecture Diagram"
with Diagram(diagram_title, **diagram):  # diagram start
    users = Users("\nUsers", **ns1)

    with Cluster("\nAWS Account", graph_attr=cs3):

        # VPC
        with Cluster("\nVPC", graph_attr=cs3):
            vpc = VPC("", **ns1)
            alb = ElbApplicationLoadBalancer("", **ns1)
            ecs = ElasticContainerService("", **ns1)

            # AVAILABILITY ZONE 1
            with Cluster("\nAvialability Zone 1", graph_attr=cs3):
                with Cluster("\nPublic Subnet 1", graph_attr=cs3):
                    public1 = PublicSubnet("Public Subnet 1", **ns1)
                with Cluster("\nPrivate Subnet 1", graph_attr=cs3):
                    ecss1 = ElasticContainerServiceService("mgmnt-app", **ns1)
                    private1 = PrivateSubnet("Private Subnet 1", **ns1)

            # AVAILABILITY ZONE 2
            with Cluster("\nAvialability Zone 2", graph_attr=cs3):
                with Cluster("\nPublic Subnet 2", graph_attr=cs3):
                    public2 = PublicSubnet("Public Subnet 2", **ns1)
                with Cluster("\nPrivate Subnet 2", graph_attr=cs3):
                    ecss2 = ElasticContainerServiceService("mgmnt-app", **ns1)
                    private2 = PrivateSubnet("Private Subnet 2", **ns1)


    # RELATION LABELS
    uses = Edge(**es2 | {"label": "uses"})
    creates = Edge(**es2 | {"label": "creates"})
    request_keys = Edge(**es2 | {"label": "request keys"})

    # COMPONENT RELATIONS
    users >> alb
    alb >> ecs >> [ecss1, ecss2]
