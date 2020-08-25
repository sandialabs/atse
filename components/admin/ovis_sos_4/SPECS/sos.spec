%global ohpc_bootstrap 1

%include %{_sourcedir}/OHPC_macros_ldms

# Set topdir to be builddir/rpm
# note this is intentionally ignored by rpmbuild. must use
# commandline syntax in makefile.am to get this effect.
#% define _topdir %(echo $PWD)/toss
# do not set unfascist build
#%-define _unpackaged_files_terminate_build 0
#%-define _missing_doc_files_terminate_build 0

%global srcname sosdb

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

# Main package
Summary: OVIS SOS Commands and Libraries
Name: ovis-sosdb
Version: 4.3.4
Release: 1.0%{?dist}
License: GPLv2 or BSD
Group: %{ldms_all}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source: %{srcname}-%{version}.tar.gz
Requires: rpm >= 4.8.0
BuildRequires: gcc glib2-devel
BuildRequires: doxygen
Url: https://github.com/ovis-hpc/sos

%description
This package provides the OVIS sosdb commands and libraries for rhel7.

%prep
%setup -q -n %{srcname}-%{version}

%build
echo bTMPPATH %{_tmppath}
rm -rf $RPM_BUILD_ROOT
echo bBUILDROOT $RPM_BUILD_ROOT
export CFLAGS=" %{optflags} -O1 -g"
%configure \
--disable-static \
--disable-python \
--enable-doc \
--enable-doc-html \
--enable-doc-man \
--enable-doc-graph

make V=1 %{?_smp_mflags}

%install
echo TMPPATH %{_tmppath}
echo BUILDROOT $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} V=1 install
ls %{buildroot}
mkdir -p %{buildroot}%{_prefix}

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/sos/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/*
%{_bindir}/*
#end core

# devel
%package devel
Summary: OVIS SOS DB devel package
Group: %{ldms_grp}
Requires: ovis-sosdb
%description devel
This is a development package of Scalable Object Store
Users who want to use sosdb from C must install this package.

%files devel
%defattr(-,root,root)
%{_includedir}/*/*.h
#end devel

%package doc
Summary: Documentation files for %{name}
Group: %{ldms_all}
%description doc
Doxygen files for ovis sosdb package.
%files doc
%defattr(-,root,root)
%{_mandir}/*/*
%{_datadir}/doc/%{srcname}
%docdir %{_datadir}/doc

%changelog
* Thu Jul 16 2020 Ben Allan <baallan@sandia.gov> 4.3.4
atse initial packaging, no python.

