%global ohpc_bootstrap 1

%include %{_sourcedir}/OHPC_macros

# Set topdir to be builddir/rpm
# note this is intentionally ignored by rpmbuild. must use
# commandline syntax in makefile.am to get this effect.
#% define _topdir %(echo $PWD)/toss
# do not set unfascist build
#%-define _unpackaged_files_terminate_build 0
#%-define _missing_doc_files_terminate_build 0

%define ldms_all System Environment/Libraries
%define build_timestamp %(date +"%Y%m%d_%H%M")
# % global __strip /bin/true
%global _enable_debug_package 0
%global _enable_debug_packages 0
%global debug_package %{nil}
%global __debug_install_post /bin/true
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%define papiversion 6.0.0

# Main package
Summary: OVIS Commands and Libraries
Name: ovis-papi
Version: %{papiversion}
Release: 1.0%{?dist}
License: GPLv2 or BSD
Group: %{ldms_all}
URL: http://icl.utk.edu/projects/papi/downloads/papi-6.0.0.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source: http://icl.utk.edu/projects/papi/downloads/papi-6.0.0.tar.gz
Requires: rpm >= 4.8.0

%description
This package provides the papi interface for LDMS

%prep
%setup -q -n papi-%{papiversion}

%build
echo bTMPPATH %{_tmppath}
rm -rf $RPM_BUILD_ROOT
echo bBUILDROOT $RPM_BUILD_ROOT
export CFLAGS="%{optflags} -O1 -g"
cd src
%configure \
--bindir=/usr/lib64/ovis-ldms/papi-%{papiversion}/bin \
--libdir=/usr/lib64/ovis-ldms/papi-%{papiversion}/lib \
--includedir=/usr/lib64/ovis-ldms/papi-%{papiversion}/include \
--mandir=/usr/lib64/ovis-ldms/papi-%{papiversion}/share/man \
--datadir=/usr/lib64/ovis-ldms/papi-%{papiversion}/share \
--datarootdir=/usr/lib64/ovis-ldms/papi-%{papiversion}/share \
--prefix=/usr/lib64/ovis-ldms/papi-%{papiversion}
make %{?_smp_mflags}

%install
echo TMPPATH %{_tmppath}
echo BUILDROOT $RPM_BUILD_ROOT
cd src
make DESTDIR=${RPM_BUILD_ROOT} V=1 install
# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/ovis-ldms/papi-%{papiversion}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/ovis-ldms/papi-%{papiversion}/lib/*
%{_libdir}/ovis-ldms/papi-%{papiversion}/share/papi/papi_events.csv
%exclude %{_libdir}/ovis-ldms/papi-%{papiversion}/lib/pkgconfig
%exclude %{_libdir}/ovis-ldms/papi-%{papiversion}/lib/pkgconfig/*
#end core

# util
%package util
Summary: LDMS PAPI util package
Group: %{ldms_grp}
Requires: ovis-papi = %{papiversion}
%description util
This is a development package of Lightweight Distributed Metric System (LDMS).
Users who want to implement their own sampler or store must install this
package.

%files util
%defattr(-,root,root)
%{_libdir}/ovis-ldms/papi-%{papiversion}/bin/*
#end util

# devel
%package devel
Summary: LDMS PAPI devel package
Group: %{ldms_grp}
Requires: ovis-papi = %{papiversion}
%description devel
This is a development package of Lightweight Distributed Metric System (LDMS).
Users who want to implement their own sampler or store must install this
package.

%files devel
%defattr(-,root,root)
%{_libdir}/ovis-ldms/papi-%{papiversion}/include/*.h
%{_libdir}/ovis-ldms/papi-%{papiversion}/include/*/*.h
%{_libdir}/ovis-ldms/papi-%{papiversion}/lib/pkgconfig/*
#end devel

%package doc
Summary: Documentation files for %{name}
Group: %{ldms_all}
%description doc
Doxygen files for ovis package.
%files doc
%defattr(-,root,root)
%{_libdir}/ovis-ldms/papi-%{papiversion}/share/man/*/*

%changelog
* Mon Mar 9 2020 Ben Allan <baallan@sandia.gov> 4.3
Create 4.3 papi software collection element.
