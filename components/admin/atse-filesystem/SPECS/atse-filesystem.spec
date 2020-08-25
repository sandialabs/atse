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

Name: atse-filesystem
Version: 1.1.0
Release: 1%{?dist}
Summary: Common top-level ATSE directories

Group: atse/admin
License: ASL 2.0

BuildArch: noarch

%description
This administrative package is used to define top level ATSE installation
directories. It is utilized by most packages that do not install into system
default paths.

%install
# The atse-filesystems owns all the common directories
mkdir -p ${RPM_BUILD_ROOT}%{OHPC_HOME}
mkdir -p ${RPM_BUILD_ROOT}%{OHPC_ADMIN}
mkdir -p ${RPM_BUILD_ROOT}%{OHPC_PUB}
mkdir -p ${RPM_BUILD_ROOT}%{OHPC_APPS}
mkdir -p ${RPM_BUILD_ROOT}%{OHPC_DOCS}
mkdir -p ${RPM_BUILD_ROOT}%{OHPC_COMPILERS}
mkdir -p ${RPM_BUILD_ROOT}%{OHPC_LIBS}
mkdir -p ${RPM_BUILD_ROOT}%{OHPC_MODULES}
mkdir -p ${RPM_BUILD_ROOT}%{OHPC_MODULEDEPS}
mkdir -p ${RPM_BUILD_ROOT}%{OHPC_MPI_STACKS}
mkdir -p ${RPM_BUILD_ROOT}%{OHPC_UTILS}
mkdir -p ${RPM_BUILD_ROOT}%{OHPC_TOOLS}

# Catch all for project specific admin files
mkdir -p ${RPM_BUILD_ROOT}%{OHPC_ADMIN}/%{PROJ_NAME}

%files
%dir %{OHPC_HOME}/
%dir %{OHPC_ADMIN}/
%dir %{OHPC_PUB}/
%dir %{OHPC_APPS}/
%dir %{OHPC_DOCS}/
%dir %{OHPC_COMPILERS}/
%dir %{OHPC_LIBS}/
%dir %{OHPC_MODULES}/
%dir %{OHPC_MODULEDEPS}/
%dir %{OHPC_MPI_STACKS}/
%dir %{OHPC_UTILS}/
%dir %{OHPC_TOOLS}/

# Catch all for project specific admin files
%dir %{OHPC_ADMIN}/%{PROJ_NAME}/
