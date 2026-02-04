# Ansible Role: Asterisk

An Ansible role to install and configure Asterisk PBX on Ubuntu systems.

## Features

- Install Asterisk from APT packages
- Configure PJSIP with multiple SIP trunks support
- Configure local endpoints (softphones, IP phones)
- Configure dialplan (extensions.conf)
- Configure voicemail with email notifications
- Handlers for restart and reload

## Requirements

- Ubuntu 24.04 (Noble) or later
- Ansible 2.16+

## Role Variables

### SIP Trunks (optional)

Configure external SIP trunks (e.g., OVH, Free, etc.):

```yaml
asterisk_pjsip_trunks:
  - name: my-trunk
    context: from-external
    server: sip.provider.com
    port: 5060
    username: "username"
    password: "password"
    codecs:
      - ulaw
      - alaw
```

### Local Endpoints

Configure local SIP endpoints for softphones and IP phones:

```yaml
asterisk_pjsip_sections:
  - name: 100
    context: internal
    username: alice
    password: "secure_password"
    codecs:        # optional, defaults to ['ulaw', 'alaw']
      - ulaw
      - alaw
    max_contacts: 1  # optional, defaults to 1
```

### Dialplan Extensions

Configure dialplan contexts and extensions:

```yaml
asterisk_extensions:
  - name: internal
    exten:
      - "_XXX,1,Dial(PJSIP/${EXTEN},20,tT)"
      - "_XXX,2,VoiceMail(${EXTEN}@internal)"
      - "_XXX,3,HangUp()"
  - name: from-external
    exten:
      - "s,1,Answer()"
      - "s,2,Playback(hello-world)"
      - "s,3,HangUp()"
```

### Voicemail

Configure voicemail boxes:

```yaml
asterisk_voicemail:
  - name: internal
    voicemail:
      - userid: 100
        password: "1234"
        mail: user@example.com
```

### Transport (optional)

Customize PJSIP transport settings:

```yaml
asterisk_transport_pjsip_name: 'transport-udp'
asterisk_transport_pjsip_protocol: 'udp'
asterisk_transport_pjsip_bind_address: '0.0.0.0'
```

### Modules

Control which Asterisk modules are loaded. Default configuration uses minimal loading for security (recommended for internet-exposed servers):

```yaml
asterisk_modules_autoload: "no"  # Only load specified modules
asterisk_modules_load:
  # Core
  - res_rtp_asterisk.so
  - res_crypto.so
  # PJSIP
  - res_pjsip.so
  - res_pjsip_session.so
  - chan_pjsip.so
  # ... (see defaults/main.yml for full list)
```

For development or internal networks, you can use autoload with exclusions:

```yaml
asterisk_modules_autoload: "yes"
asterisk_modules_noload:
  - chan_sip.so
  - chan_skinny.so
  - chan_mgcp.so
```

### Music on Hold (optional)

Configure music on hold classes with custom audio files:

```yaml
asterisk_musiconhold:
  - name: default
    mode: files
    directory: /var/lib/asterisk/moh
    files:
      - files/moh/music1.wav
      - files/moh/music2.wav
  - name: waiting
    mode: files
    directory: /var/lib/asterisk/moh-waiting
    random: "yes"
    files:
      - files/moh-waiting/hold1.wav
```

Place your audio files in `files/moh/` in your playbook directory.

## Dependencies

None.

## Example Playbook

```yaml
- hosts: pbx
  roles:
    - role: ansible-role-asterisk
      vars:
        asterisk_pjsip_trunks:
          - name: ovh
            context: from-external
            server: sip.ovh.fr
            username: "0033xxxxxxxxx"
            password: "your_password"

        asterisk_pjsip_sections:
          - name: 100
            context: internal
            username: alice
            password: "alice_password"
          - name: 101
            context: internal
            username: bob
            password: "bob_password"

        asterisk_extensions:
          - name: internal
            exten:
              - "_1XX,1,Dial(PJSIP/${EXTEN},20,tT)"
              - "_1XX,2,HangUp()"
```

## Testing

This role uses Molecule for testing with Vagrant/libvirt:

```bash
# Run full test sequence
molecule test

# Create and converge only
molecule converge

# Run tests
molecule verify

# Destroy test environment
molecule destroy
```

## Handlers

| Handler | Description |
|---------|-------------|
| `Restart asterisk` | Full service restart (interrupts calls) |
| `Reload asterisk` | Reload configuration (preserves active calls) |

## License

MIT / BSD

## Author

Michael MACHADO
