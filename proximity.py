##
import bluetooth

def proximity():
    print("Performing inquiry...")
    addList = []

    nearby_devices = bluetooth.discover_devices(
            duration=12, lookup_names=True, flush_cache=True)
    print("found %d devices" % len(nearby_devices))

    for addr, name in nearby_devices:
        try:
            print(" %s - %s" % (addr, name))
            addList.append(addr)
        except UnicodeEncodeError:
            print(" %s - %s" % (addr, name.encode('utf-8', 'replace')))
    return addList        


#
#
