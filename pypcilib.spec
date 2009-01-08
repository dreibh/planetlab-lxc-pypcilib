#
# $Id$
#
%define url $URL$

%define name pypcilib
%define version 0.2
%define taglevel 5

%define release %{taglevel}%{?pldistro:.%{pldistro}}%{?date:.%{date}}

%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: Python library for doing PCI stuff
Name: %{name}
Version: %{version}
Release: %{release}
License: BSD
Group: System Environment/Libraries

Packager: PlanetLab Central <support@planet-lab.org>
Distribution: PlanetLab %{plrelease}
#URL: http://svn.planet-lab.org/wiki/pypcilib
URL: %(echo %{url} | cut -d ' ' -f 2)

Source0: pypcilib-%{version}.tar.bz2

Requires: /sbin/lspci

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(id -un)

%description
pypcilib is a Python library to scan PCI devices using
libpci from pciutils, and to parse the modules.pcimap file.


%prep
%setup -q


%build
%{__python} setup.py build


%install
rm -fr "%{buildroot}"
%{__python} setup.py install -O1 --skip-build --root "%{buildroot}"
touch %{buildroot}%{python_sitelib}/pypcimap.py{c,o}
touch %{buildroot}%{python_sitelib}/pypci.py{c,o}


%clean
rm -fr "%{buildroot}"


%files
%defattr(-,root,root,-)
%{python_sitelib}/pypcimap.py
%ghost %{python_sitelib}/pypcimap.pyc
%ghost %{python_sitelib}/pypcimap.pyo
%{python_sitelib}/pypci.py
%ghost %{python_sitelib}/pypci.pyc
%ghost %{python_sitelib}/pypci.pyo
# xxx - quick'n dirty
%if "%{distroname}" == "f9" || "%{distroname}" == "f10"
%{python_sitelib}/pypciscan*.egg-info
%endif


%changelog
* Thu Jan 08 2009 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - pypcilib-0.2-5
- support for building on fedora 10

* Thu Dec 04 2008 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - pypcilib-0.2-4
- somehow the versions in the specfile are wrong in tag 0.2-3

* Wed Sep 10 2008 Thierry Parmentelat <thierry.parmentelat@sophia.inria.fr> - pypcilib-0.2-2
- fixes for building on f9/gcc-4.3 - no functional change

* Fri Mar 14 2008 Daniel Hokka Zakrisson <daniel@hozac.com> - 0.2-1
- Remove pypciscan library, reimplemented in Python

* Mon Nov 19 2007 Daniel Hokka Zakrisson <daniel@hozac.com> - 0.1-1
- initial release
