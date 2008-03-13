import os
try:
    from pypciscan import get_devices
except:
    def get_devices():
        """ This is a replacement to the version in pypciscan library for 3.3 and lower bootcds 
        that will help maintain backward compatibility.  This version has limitations wrt accuracy
        that the library does not.  In particular it is limited to the output of
        lspci and 'forces' all devices to appear on the '0000' domain, rather than
        where they actually are."""

        ret = {}
        pci_cmd = os.popen("""/sbin/lspci -nvm | sed -e 's/\t/ /g' -e 's/ Class //' -e 's/^/"/' -e 's/$/"/' -e 's/$/,/' -e 's/^"",$/],[/'""", 'r')
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
            print dev
            if 'device' not in dev:
                continue

            if 'sdevice' in dev: subdev = dev['sdevice']
            else: subdev = 0xffffffffL

            if 'svendor' in dev: subvend = dev['svendor']
            else: subvend = 0xffffffffL

            key = "0000:%s" % dev['deviceaddr']
            value = (dev['vendor'], dev['device'], subvend, subdev, dev['class'] << 8)
            ret[key] = value

        return  ret

import pypcimap
