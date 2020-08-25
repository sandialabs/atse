%global ohpc_bootstrap 1

%include %{_sourcedir}/OHPC_macros

Summary: Package that installs Ovis LDMS
Name: ovis_ldms
Version: 4.3.4
Release: 1.1%{?dist}
License: GPLv2+
Requires: ovis-papi
Requires: ovis-sos
Requires: ovis-ldms
Requires: ovis-ldms-initscripts-base
Requires: ovis-ldms-initscripts-systemd
Requires: ovis-ldms-plugins-llnl

%description
This bundles ldms with hpc-oriented samplers and stores for TOSS3 style distribution


%changelog
* Thu Jul 16 2020 Benjamin Allan <baallan@sandia.gov> 0.1
- added sosdb
* Wed Apr 15 2020 Benjamin Allan <baallan@sandia.gov> 0.1
- revised package dependencies
