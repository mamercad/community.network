#!/usr/bin/python
#  -*- coding: utf-8 -*-
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import env_fallback
from ansible.module_utils.compat.paramiko import paramiko
from ansible.module_utils._text import to_native, to_text
import time

__metaclass__ = type


def status(module, pihole, username, password):
    try:
        buf = ''
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(pihole, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(
            'echo $TERM; /usr/local/bin/pihole status')
        while not stdout.channel.exit_status_ready() and not stdout.channel.recv_ready():
            time.sleep(1)
        buf += ''.join(stdout.readlines())
        client.close()
    except Exception as e:
        module.fail_json(msg=to_text(e))
    return buf


def main():
    if paramiko is None:
        module.fail_json(
            msg='The paramiko library is required for this module')

    argument_spec = dict(
        pihole=dict(type=str, default='localhost'),
        username=dict(type=str, default='pi'),
        password=dict(type=str, default='raspberry'),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=False)

    pihole = module.params['pihole']
    username = module.params['username']
    password = module.params['password']

    module.exit_json(changed=True, msg=status(
        module, pihole, username, password))


if __name__ == '__main__':
    main()
