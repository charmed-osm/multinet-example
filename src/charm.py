#!/usr/bin/env python3
# Copyright 2021 David Garcia
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following post for a quick-start guide that will help you
develop a new k8s charm using the Operator Framework:

    https://discourse.charmhub.io/t/4208
"""

import json
import logging

from ops.charm import CharmBase
from ops.main import main
from ops.framework import StoredState
from ops.model import ActiveStatus, BlockedStatus

logger = logging.getLogger(__name__)


class MultinetCharm(CharmBase):
    """Charm the service."""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.leader_elected, self.configure_pod)
        self.framework.observe(self.on.config_changed, self.configure_pod)

    def configure_pod(self, _):
        if not self.unit.is_leader():
            self.unit.status = ActiveStatus()
            return
        networks = []
        static_ips = {}
        for net_ip in self.config.get("static_ips", "").split(","):
            if not net_ip:
                continue
            if ":" in net_ip:
                network_name, static_ip = net_ip.split(":")
                static_ips[network_name] = static_ip
            else:
                self.unit.status = BlockedStatus("Wrong format in static_ips")
                return
        for net in self.config.get("networks", "").split(","):
            if not net:
                continue
            interface_name = None
            if ":" in net:
                network_name, interface_name = net.split(":")
            else:
                network_name = net
            network = {"name": network_name}
            if interface_name:
                network["interface"] = interface_name
            if network_name in static_ips:
                network["ips"] = [static_ips[network_name]]
            networks.append(network)

        pod_spec = {
            "version": 3,
            "containers": [
                {
                    "name": "multinet",
                    "image": "alpine:latest",
                    "imagePullPolicy": "Always",
                    "ports": [
                        {
                            "name": "dummy",
                            "containerPort": 80,
                            "protocol": "TCP",
                        }
                    ],
                    "command": ["sh"],
                    "args": ["-c", "while [ true ]; do ifconfig; sleep 3; done"]
                }
            ],
            "kubernetesResources": {
                "pod": {
                    "annotations": {"k8s.v1.cni.cncf.io/networks": json.dumps(networks)}
                },
            },
        }
        self.model.pod.set_spec(pod_spec)
        self.unit.status = ActiveStatus()


if __name__ == "__main__":
    main(MultinetCharm)
