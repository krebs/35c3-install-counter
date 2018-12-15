# 35c3 NixOS Installation Counter
Counts the NixOS installations on the 35c3.

## Usage

### Development

New Installation annoucement via Spacebar, no sending to IRC: `./curs.py --input=space`

### Production

Use Button with serial interface, send to IRC:

```
./curs.py --token '<matrix.org-token>' --channel '#freenode_#nixos-de:matrix.org'
```

#### Get the matrix.org token
```
curl -XPOST -d '{"type":"m.login.password", "user":"USER", "password":"PW"}' "https://matrix.org/_matrix/client/r0/login"
```
