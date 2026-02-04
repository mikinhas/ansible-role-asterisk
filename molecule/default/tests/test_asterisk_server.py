import pytest


def test_asterisk_is_installed(host):
    """Test that asterisk package is installed."""
    asterisk = host.package("asterisk")
    assert asterisk.is_installed


def test_asterisk_running_and_enabled(host):
    """Test that asterisk service is running and enabled."""
    asterisk = host.service("asterisk")
    assert asterisk.is_running
    assert asterisk.is_enabled


@pytest.mark.parametrize("config_file", [
    "/etc/asterisk/asterisk.conf",
    "/etc/asterisk/modules.conf",
    "/etc/asterisk/pjsip.conf",
    "/etc/asterisk/extensions.conf",
    "/etc/asterisk/voicemail.conf",
    "/etc/asterisk/musiconhold.conf",
])
def test_asterisk_config_files_exist(host, config_file):
    """Test that asterisk configuration files exist with correct permissions."""
    config = host.file(config_file)
    assert config.exists
    assert config.user == "asterisk"
    assert config.group == "asterisk"
    assert config.mode == 0o640


def test_pjsip_transport_config(host):
    """Test that pjsip.conf contains transport configuration."""
    pjsip_conf = host.file("/etc/asterisk/pjsip.conf")
    assert pjsip_conf.contains("type=transport")
    assert pjsip_conf.contains("protocol=udp")
    assert pjsip_conf.contains("bind=0.0.0.0")


def test_pjsip_endpoints_config(host):
    """Test that pjsip.conf contains local endpoints."""
    pjsip_conf = host.file("/etc/asterisk/pjsip.conf")
    assert pjsip_conf.contains("type=endpoint")
    assert pjsip_conf.contains("type=auth")
    assert pjsip_conf.contains("type=aor")


def test_modules_config(host):
    """Test that modules.conf has minimal secure configuration."""
    modules_conf = host.file("/etc/asterisk/modules.conf")
    assert modules_conf.contains("autoload=no")
    assert modules_conf.contains("load => res_pjsip.so")
    assert modules_conf.contains("load => chan_pjsip.so")
