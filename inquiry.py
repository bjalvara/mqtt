#performs a simple device inquiry followed by a remote name of each discovered  device

import bluetooth

print("performing inquiry...")
nearby_devices = bluetooth.discover_devices(
    duration=3, lookup_names=True, flush_cache=True)


print("found %d devices" % len(nearby_devices))

for addr, name in nearby_devices:
    try:
        print(" %s - %s" % (addr, name))
    except UnicodeDecodeError:
        print(" %s -%s" % (addr,name.encode('utf-8', 'replace')))