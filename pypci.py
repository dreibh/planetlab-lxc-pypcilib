import os

def get_devices():
    """ This is a replacement to the pypciscan library."""

    ret = {}
    pci_cmd = os.popen("""/sbin/lspci -Dnvm | sed -e 's/\t/ /g' -e 's/^/"/' -e 's/$/"/' -e 's/$/,/' -e 's/^"",$/],[/'""", 'r')
    pci_str = "[" + pci_cmd.read() + "]"
    pci_list = eval(pci_str)

    pci_devlist = []
    # convert each entry into a dict. and convert strings to ints.
    for dev in pci_list:
        rec = {}
        for field in dev:
            s = field.split(":")
            if len(s) > 2:
                # There are two 'device' fields in the output. Append
                # 'addr' for the bus address, identified by the extra ':'.
                end=":".join(s[1:])
                key = s[0].lower() + "addr"
                value = end.strip()
            else:
                key = s[0].lower()
                value = int(s[1].strip(), 16)

            rec[key] = value

        pci_devlist.append(rec)

    ret = {}
    # convert this list of devices into the format expected by the
    # consumer of get_devices()
    for dev in pci_devlist:
        if 'deviceaddr' not in dev:
            continue

        if 'sdevice' in dev: subdev = dev['sdevice']
        else: subdev = 0xffffffffL

        if 'svendor' in dev: subvend = dev['svendor']
        else: subvend = 0xffffffffL

        if 'progif' in dev: progif = dev['progif']
        else: progif = 0

        value = (dev['vendor'], dev['device'], subvend, subdev, dev['class'] << 8 | progif)
        ret[dev['deviceaddr']] = value

    return  ret

import pypcimap
