
import os

testinfra_hosts = ["asterisk-server-noble"]

def test_asterisk_is_installed(host):
    asterisk = host.package("asterisk")
    assert asterisk.is_installed

def test_asterisk_running_and_enabled(host):
    asterisk = host.service("asterisk")
    assert asterisk.is_running
    assert asterisk.is_enabled

def test_asterisk_config_exists(host):
    config = host.file("/etc/asterisk/asterisk.conf")
    assert config.exists
    assert config.user == "asterisk"
    assert config.group == "asterisk"
    assert config.mode == 0o640

    pjsip_conf = host.file("/etc/asterisk/pjsip.conf")
    assert pjsip_conf.exists
    assert pjsip_conf.contains("protocol=udp")
    assert pjsip_conf.contains("bind=0.0.0.0")