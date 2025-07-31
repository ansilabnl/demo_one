#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022-2025, Ton Kersten
# GNU General Public License v3.0
# see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt
#
"""Find host that runs Ansible

Get the fqdn of the Ansible control node
"""

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import socket

__metaclass__ = type


ANSIBLE_METADATA = {
    "metadata_version": "0.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
  lookup: play_host
  short_description: return fqdn of the control node
  author:
    - Ton Kersten <tonk@smartowl.nl>
  version_added: "2.11"
  description:
    - Return the fqdn of the control node
"""

EXAMPLES = r"""
- name: Generate the motd
  ansble.builtin.set_fact:
      play_host: "{{ lookup('play_host') }}"
"""

RETURN = r"""
message:
    description: fqdn of control node
    type: str
    returned: always
"""

display = Display()


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):

        return [socket.getfqdn()]
