%global ohpc_bootstrap 1

%include %{_sourcedir}/OHPC_macros_ldms

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
%define pluginsllnlversion 1.5
%define ldmsversion 4.3.4

# Main package
Summary: OVIS Commands and Libraries
Name: ovis-ldms-plugins-llnl
Version: %{ldmsversion}
Release: 1.0%{?dist}
License: GPLv2 or BSD
Group: %{ldms_all}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source: ldms-plugins-llnl-1.5.tar.gz
# https://github.com/LLNL/ldms-plugins-llnl/releases/download/1.5/ldms-plugins-llnl-1.5.tar.gz
Requires: ovis-ldms
BuildRequires: ovis-ldms-devel
Requires: rpm >= 4.8.0

%description
This package provides the llnl lustre plugins for LDMS

%prep
%setup -q -n ldms-plugins-llnl-1.5

%build
echo bTMPPATH %{_tmppath}
rm -rf $RPM_BUILD_ROOT
echo bBUILDROOT $RPM_BUILD_ROOT
export CFLAGS="%{optflags} -O1 -g"

%configure
make %{?_smp_mflags}

%install
echo TMPPATH %{_tmppath}
echo BUILDROOT $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} V=1 install
# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/ovis-ldms/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/ovis-ldms/*
#end core

%package doc
Summary: Documentation files for %{name}
Group: %{ldms_all}
%description doc
Man pages for llnl package.
%files doc
%defattr(-,root,root)
%{_mandir}/*/*

%changelog
* Mon Mar 9 2020 Ben Allan <baallan@sandia.gov> 4.3
Create 4.3 llnl lustre plugins package for ldms
