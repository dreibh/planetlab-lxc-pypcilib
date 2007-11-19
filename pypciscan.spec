%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Scan PCI devices from Python
Name: pypciscan
Version: 0.1
Release: 1
License: BSD
URL: http://svn.planet-lab.org/wiki/pypciscan
Group: System Environment/Libraries

BuildRequires: pciutils-devel

Source0: pypciscan-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -un)


%description
pypciscan is a Python library to scan PCI devices using
pciutils' libpci.


%prep
%setup -q


%build
CFLAGS="%{optflags}" %{__python} setup.py build


%install
rm -fr "%{buildroot}"
%{__python} setup.py install -O1 --skip-build --root "%{buildroot}"


%clean
rm -fr "%{buildroot}"


%files
%defattr(-,root,root,-)
%{python_sitearch}/pypciscan.so


%changelog
* Mon Nov 19 2007 Daniel Hokka Zakrisson <daniel@hozac.com> - 0.1-1
- initial release
