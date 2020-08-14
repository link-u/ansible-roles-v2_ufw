import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_ufw_is_installed(host):
    ufw = host.package("ufw")
    assert ufw.is_installed

def test_ufw_running_and_enabled(host):
    ufw = host.service("ufw")
    assert ufw.is_running
    assert ufw.is_enabled

def test_white_ip_list(host):
    ansible_vars = host.ansible.get_variables()
    ufw_white_ip_list = ansible_vars["ufw_white_ip_list"]

    for ufw_white_ip in ufw_white_ip_list:
        assert not host.ansible(
            "ufw",
            "rule=allow " +
            "from=" + ufw_white_ip)["changed"]

def test_white_port_settings(host):
    ansible_vars = host.ansible.get_variables()
    ufw_port_settings = ansible_vars["ufw_port_settings"]

    for ufw_port in ufw_port_settings:
        to_port  = ufw_port["to_port"]
        rule     = ufw_port.get("rule", "allow")
        proto    = ufw_port.get("proto", "tcp")
        for from_ip in ufw_port["from_ip_list"]:
            assert not host.ansible(
                "ufw",
                "to_port=" + to_port + " " +
                "rule=" + rule + " " +
                "proto=" + proto + " " +
                "from_ip=" + from_ip)["changed"]
