%global ohpc_bootstrap 1

%include %{_sourcedir}/OHPC_macros

%global scl_name_prefix sandia-nosos-
%global scl_name_base ovis_ldms_
%global scl_name_version 4.3.3
%global scl %{scl_name_prefix}%{scl_name_base}%{scl_name_version}

# Optional but recommended: define nfsmountable
%global nfsmountable 1

%global _scl_prefix /opt/ovis
%scl_package %scl

Summary: Package that installs %scl
Name: %{scl_name}
Version: 1
Release: 1%{?dist}
License: GPLv2+
Requires: %{scl_prefix}ovis-ldms
Requires: %{scl_prefix}ovis-ldms-initscripts-base
Requires: %{scl_prefix}ovis-ldms-initscripts-systemd

BuildRequires: scl-utils-build

%description
This is the main package for %scl Software Collection.

%package runtime
Summary: Package that handles %scl Software Collection.
Requires: scl-utils

%description runtime
Package shipping items to work with %scl Software Collection.

%package build
Summary: Package shipping basic build configuration
Requires: scl-utils-build

%description build
Package shipping essential configuration macros to build %scl Software Collection.

%package scldevel
Summary: Package shipping development files for %scl

%description scldevel
Package shipping development files, especially useful for development of
plugin packages depending on %scl Software Collection.

%prep
%setup -c -T

%install
%scl_install

mkdir -p %{buildroot}%{_scl_scripts}
cat >> %{buildroot}%{_scl_scripts}/enable << EOF
export PATH="%{_bindir}:%{_sbindir}\${PATH:+:\${PATH}}"
export LD_LIBRARY_PATH="%{_libdir}\${LD_LIBRARY_PATH:+:\${LD_LIBRARY_PATH}}"
export MANPATH="%{_mandir}:\${MANPATH:-}"
export PYTHONPATH="%{_scl_root}%{python_sitearch}:%{_scl_root}%{python_sitelib}\${PYTHONPATH:+:}\${PYTHONPATH:-}"
EOF

# This is only needed when you want to provide an optional scldevel subpackage
cat >> %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel << EOF
%%scl_%{scl_name_base} %{scl}
%%scl_prefix_%{scl_name_base} %{scl_prefix}
EOF

# Install the not generated man page
# nothing.

%files

%files runtime -f filelist
%scl_files


%files build
%{_root_sysconfdir}/rpm/macros.%{scl}-config

%files scldevel
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel

%changelog
* Mon Dec 9 2019 Benjamin Allan <baallan@sandia.gov> 0.2
- revised package dependencies
* Thu Oct 17 2019 Benjamin Allan <baallan@sandia.gov> 0.1
- Initial package
