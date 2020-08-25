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

Name:      atse-buildroot
Version:   1.2.0
Release:   1%{?dist}
Summary:   Common build scripts used in ATSE packaging
Group:     atse/admin
License:   ASL 2.0
Source0:   ATSE_setup_compiler
Source1:   ATSE_setup_mpi
Source2:   atse-find-requires
Source3:   atse-find-provides
Source4:   atse-find-requires-perllib
Source5:   atse-find-provides-perllib
BuildArch: noarch

BuildRequires: atse-filesystem
Requires:      atse-filesystem
Requires:      lmod-atse

%description
This administrative package is used to provide RPM dependency analysis tools
and common compiler and MPI family convenience scripts used during ATSE
builds.

%install
# The atse-filesystem package owns all the common directories
mkdir -p ${RPM_BUILD_ROOT}/usr/lib/rpm/fileattrs
mkdir -p ${RPM_BUILD_ROOT}/%{OHPC_ADMIN}/%{PROJ_NAME}

install -p -m 644 %{SOURCE0} ${RPM_BUILD_ROOT}%{OHPC_ADMIN}/%{PROJ_NAME}
install -p -m 644 %{SOURCE1} ${RPM_BUILD_ROOT}%{OHPC_ADMIN}/%{PROJ_NAME}

# rpm dependency plugins
install -p -m 755 %{SOURCE2} $RPM_BUILD_ROOT/usr/lib/rpm
install -p -m 755 %{SOURCE3} $RPM_BUILD_ROOT/usr/lib/rpm
install -p -m 755 %{SOURCE4} $RPM_BUILD_ROOT/usr/lib/rpm
install -p -m 755 %{SOURCE5} $RPM_BUILD_ROOT/usr/lib/rpm

%{__mkdir_p} %{buildroot}/usr/lib/rpm/fileattrs/

# ELF-LIB File Attribute Classification
%{__cat} <<EOF > %{buildroot}//usr/lib/rpm/fileattrs/atse.attr
%%__atse_provides        /usr/lib/rpm/atse-find-provides
%%__atse_requires        /usr/lib/rpm/atse-find-requires %%{buildroot} %{OHPC_HOME}

%%__atse_path            ^%{OHPC_HOME}
%%__elf_exclude_path     ^%{OHPC_HOME}

%%__atse_magic           ^ELF (32|64)-bit.*$
%%__atse_flags           magic_and_path
EOF

%if 0%{?sles_version} || 0%{?suse_version}
%{__cat} <<EOF >> %{buildroot}//usr/lib/rpm/fileattrs/atse.attr
%%__elflib_exclude_path  ^%{OHPC_HOME}
EOF
%endif

# Perl File Attribute Classification
%{__cat} <<EOF > %{buildroot}//usr/lib/rpm/fileattrs/atseperllib.attr
%%__atseperllib_provides     /usr/lib/rpm/atse-find-provides-perllib
%%__atseperllib_requires     /usr/lib/rpm/atse-find-requires-perllib %%{buildroot} %{OHPC_HOME}

%%__atseperllib_path         ^%{OHPC_HOME}
%%__perllib_exclude_path     ^%{OHPC_HOME}
%%__perl_exclude_path        ^%{OHPC_HOME}

%%__atseperllib_magic        ^Perl[[:digit:]] module source.*
%%__atseperllib_flags        magic_and_path
EOF

%files
%dir /usr/lib/rpm/
%dir /usr/lib/rpm/fileattrs/
%{OHPC_ADMIN}/%{PROJ_NAME}/ATSE_setup_compiler
%{OHPC_ADMIN}/%{PROJ_NAME}/ATSE_setup_mpi
/usr/lib/rpm/atse-find-provides
/usr/lib/rpm/atse-find-requires
/usr/lib/rpm/fileattrs/atse.attr
/usr/lib/rpm/atse-find-provides-perllib
/usr/lib/rpm/atse-find-requires-perllib
/usr/lib/rpm/fileattrs/atseperllib.attr
