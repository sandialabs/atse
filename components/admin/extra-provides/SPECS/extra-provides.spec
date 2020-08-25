#----------------------------------------------------------------------------bh-
# This RPM .spec file is part of the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%global ohpc_bootstrap 1

%include %{_sourcedir}/OHPC_macros

Name: extra-provides
Version: 1.0.0
Release: 1%{?dist}
Summary: Extra provides required for ATSE

Group: atse/admin
License: ASL 2.0

BuildArch: noarch

Source0: extra-provides

Provides: libstdc++.so.6(GLIBCXX_3.4.26)(64bit)
Provides: srptools = 41mlnx1-5.46101
Provides: ibsim = 0.7mlnx1-0.11.g85c342b.46101

%description
This administrative package to add extra provides to resolve
rpm dependency hell.  Ideally this package provides no extra
provides, however in practice there are often extra provides
needed in order to install other ATSE packages.

%install
%{__mkdir_p} %{buildroot}/%{OHPC_LIBS}/${pname}/%{version}
install -p -m 644 %{SOURCE0} %{buildroot}/%{OHPC_LIBS}/${pname}/%{version}/extra-provides

%files
%{OHPC_PUB}
