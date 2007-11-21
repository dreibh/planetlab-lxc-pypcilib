/* Copyright 2007 The Trustees of Princeton University

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met: 

* Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
      
* Redistributions in binary form must reproduce the above
copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided
with the distribution.
      
* Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived
from this software without specific prior written permission.
      
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL PRINCETON
UNIVERSITY OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE. 

*/

#include <Python.h>

#include <stdio.h>
#include <stdlib.h>

#include <pci/pci.h>


static PyObject *get_devices(PyObject *self, PyObject *args)
{
	struct pci_access *pacc;
	struct pci_dev *dev;
	PyObject *ret;
	char buf[128];

	if ((pacc = pci_alloc()) == NULL)
		return PyErr_SetFromErrno(PyExc_OSError);

	pci_init(pacc);

	pci_scan_bus(pacc);

	ret = PyDict_New();
	if (!ret)
		return PyErr_SetFromErrno(PyExc_OSError);

	for (dev = pacc->devices; dev; dev = dev->next) {
		u16 subvendor = -1, subdevice = -1;
		PyObject *value;
		u8 progif = 0;

		pci_fill_info(dev, PCI_FILL_IDENT | PCI_FILL_CLASS);
		if (dev->hdrtype == PCI_HEADER_TYPE_NORMAL) {
			subvendor = pci_read_word(dev, PCI_SUBSYSTEM_VENDOR_ID);
			subdevice = pci_read_word(dev, PCI_SUBSYSTEM_ID);
		}
		progif = pci_read_byte(dev, PCI_CLASS_PROG);

		snprintf(buf, sizeof(buf), "%04x:%02x:%02x.%02x", dev->domain, dev->bus, dev->dev, dev->func);
		value = Py_BuildValue("iiiii", dev->vendor_id, dev->device_id,
				      subvendor, subdevice, dev->device_class << 8 | progif);
		if (!value)
			return NULL;
		if (PyDict_SetItemString(ret, buf, value) == -1)
			return NULL;
	}

	return ret;
}


static PyMethodDef methods[] = {
	{ "get_devices", get_devices, METH_VARARGS,
	  "Returns a dict of PCI devices, indexed by the domain:bus:dev.func string, "
	  "each item consisting of [vendor, device, subvendor, subdevice, class]" },
	{ NULL, NULL, 0, NULL }
};

PyMODINIT_FUNC
initpypciscan(void)
{
	PyObject *mod;
	mod = Py_InitModule("pypciscan", methods);
}
