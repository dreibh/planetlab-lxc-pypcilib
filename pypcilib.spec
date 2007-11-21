%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Python library for doing PCI stuff
Name: pypcilib
Version: 0.1
Release: 1
License: BSD
URL: http://svn.planet-lab.org/wiki/pypcilib
Group: System Environment/Libraries

BuildRequires: pciutils-devel

Source0: pypcilib-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -un)


%description
pypcilib is a Python library to scan PCI devices using
pciutils' libpci, and to parse the modules.pcimap file.


%prep
%setup -q


%build
CFLAGS="%{optflags}" %{__python} setup.py build


%install
rm -fr "%{buildroot}"
%{__python} setup.py install -O1 --skip-build --root "%{buildroot}"
touch %{buildroot}%{python_sitearch}/pypcimap.py{c,o}


%clean
rm -fr "%{buildroot}"


%files
%defattr(-,root,root,-)
%{python_sitearch}/pypciscan.so
%{python_sitearch}/pypcimap.py
%ghost %{python_sitearch}/pypcimap.pyc
%ghost %{python_sitearch}/pypcimap.pyo


%changelog
* Mon Nov 19 2007 Daniel Hokka Zakrisson <daniel@hozac.com> - 0.1-1
- initial release
